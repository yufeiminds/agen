# coding=utf8

__version__ = '0.1.1'
__author__ = 'Yufei Li <yufeiminds@163.com>'
__all__ = [
    'string_render', 'render',
    'generate', 'generate_dir'
]

"""
Code Generator
~~~~~~~~~~~~~~

:copyright: (c) 2016 Yufei Li
"""

import os
import re
import six
import json
import yaml
import click
import jinja2
import chardet
import logging
import subprocess

# Initialize globals
logging.basicConfig()
logger = logging.getLogger('agen')
app_folder = click.get_app_dir("agen", force_posix=True)


class Coderes(object):
    @classmethod
    def read(cls, obj, as_encoding=None):
        """
        Read as unicode
        """
        content = obj.read()
        if six.PY3:
            return content
        confidences = chardet.detect(content)
        _confidence, _encoding = [0, 'utf-8']
        for confidence, encoding in six.iteritems(confidences):
            if confidence > _confidence:
                _confidence, _encoding = confidence, encoding
        if as_encoding:
            return content.decode(_encoding).encode(as_encoding)
        return content.decode(_encoding)


class AbsLoader(jinja2.loaders.BaseLoader):
    """
    A loader use absolute path for jinja2.

    see _`http://jinja.pocoo.org/docs/dev/api/#loaders`
    """

    def __init__(self):
        pass

    def get_source(self, environment, template):
        path = template
        if not os.path.exists(path):
            raise jinja2.exceptions.TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path) as f:
            source = Coderes.read(f)

        return source, path, lambda: mtime == os.path.getmtime(path)


class agenError(Exception):
    """
    agen exception.
    """
    pass


TEMPLATED_PARTTERN = re.compile(r'{{[^}]+}}')


def string_render(string, context, jinja_env=None):
    """
    Straight to render a template string.

    :param string: a template string
    :param context: context variable will be render
    :return: string be rendered
    """
    _env = jinja_env or jinja2.Environment(loader=AbsLoader())
    _context = context or {}

    if TEMPLATED_PARTTERN.search(string):
        return _env.from_string(string).render(_context)
    return string


def render(template_file, context=None, jinja_env=None):
    """
    Render string from :mod:`jinja2` template file.

    :param template_file: path of template file.
    :param context: context dictionary
    :param jinja_env: :class:`jinja2.Environment` object.
    :return: rendered text
    """
    _env = jinja_env or jinja2.Environment(loader=AbsLoader())
    _context = context or {}

    template = _env.get_template(template_file)
    return template.render(_context)


def generate(template_file, out, context=None, jinja_env=None):
    """
    Generate a pure text file from :mod:`jinja2` template file.

    :param template_file: path of template file.
    :param out: path of output file
    :param context: context dictionary
    :param jinja_env: :class:`jinja2.Environment` object.
    """
    _env = jinja_env or jinja2.Environment(loader=AbsLoader())
    _context = context or {}

    outdir = os.path.dirname(out)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    with open(out, 'w') as f:
        text = render(template_file, context=_context, jinja_env=_env)
        if six.PY2:
            text = text.encode('utf-8')
        f.write(text)


def generate_dir(directory, out, context=None, jinja_env=None):
    """
    Generate a directory from :mod:`jinja2` template directory.

    :param template_file: path of template file.
    :param out: path of output file
    :param context: context dictionary
    :param jinja_env: :class:`jinja2.Environment` object.
    """
    loader = jinja2.FileSystemLoader(directory)
    _env = jinja_env or jinja2.Environment(loader=loader)
    _context = context or {}

    for dirname, _, fnames in os.walk(directory):
        reldir = os.path.relpath(dirname, directory)
        for name in fnames:
            relpath = os.path.join(reldir, name)
            relout = string_render(relpath, _context)
            relout = os.path.join(out, relout)
            generate(relpath, relout, context=_context, jinja_env=_env)


def choice(directory, files):
    """
    :param directory: directory of files in.
    :param files: list of file be choice
    :return: first existed path
    """
    for name in files:
        fpath = os.path.join(directory, name)
        if os.path.exists(fpath):
            return fpath
    return None


def load_context(path):
    """
    load context file
    """
    with open(path) as f:
        if path.endswith('.json'):
            return json.load(f)
        if path.endswith('.yaml'):
            return yaml.load(f)
    return {}


def prompt(dictionary):
    """
    Interactive input for dictionary sample data

    :param dictionary: key-value pair that will be prompted
    """
    _dictionary = {}
    for key, value in six.iteritems(dictionary):
        _dictionary[key] = click.prompt(key, default=value,
                                        type=type(value))
    return _dictionary


class Path(object):
    """
    Path validator
    """
    def __init__(self, path):
        self.path = path
        assert os.path.exists(path)

    @property
    def is_single(self):
        return os.path.isfile(self.path)

    @property
    def is_repo(self):
        try:
            return bool(self.inner) and (self.context is not None)
        except AssertionError:
            return False

    @property
    def is_dir(self):
        return os.path.isdir(self.path) and not self.is_repo

    @property
    def inner(self):
        assert os.path.isdir(self.path)
        for name in os.listdir(self.path):
            inner = os.path.join(self.path, name)
            if os.path.isdir(inner):
                return inner
        return None

    @property
    def context(self):
        assert os.path.isdir(self.path)
        conf = choice(self.path, ['agen.json', 'agen.yaml'])
        if not conf:
            return None
        return load_context(conf)


def _prompt_app_folder(folder):
    folder_prompt = "  see -> {tf}".format(tf=folder)
    click.secho("-" * (len(folder_prompt) + 2), fg='blue')
    click.secho("  agen Library", fg='blue')
    click.secho(folder_prompt, fg='blue')
    click.secho("-" * (len(folder_prompt) + 2), fg='blue')


@click.command()
@click.option('-o', '--out', type=click.Path(), help="Output path or directory")
@click.option('-s', '--source', type=click.Path(exists=True), help="Source path or directory")
@click.option('-c', '--context', type=click.Path(exists=True), help="Path of context file")
@click.argument('name', nargs=-1)
def cli(out, source, context, name):
    _context = {}
    tf = os.path.join(app_folder, "templates")

    if not os.path.exists(app_folder):
        os.mkdir(app_folder)
        os.mkdir(tf)
        click.secho("Creating {af} ...".format(af=app_folder), fg="green")

    if not (source or name):
        _prompt_app_folder(tf)
        subprocess.check_call(
            'ls ' + os.path.join(app_folder, "templates"),
            shell=True)
        exit(0)

    if not out:
        out = click.prompt('Output directory', default=os.path.curdir)

    try:
        path = Path(source or os.path.join(tf, name[0]))
    except AssertionError:
        click.secho("\nThis path does not exist", fg='red')
        return

    if context:
        _context.update(load_context(context))

    if path.is_repo:
        if not context:
            _context.update(prompt(path.context))
        inner = path.inner
        out_name = string_render(os.path.split(inner)[-1], _context)
        out = os.path.join(out, out_name)
        generate_dir(inner, out, context=_context)

    if path.is_dir:
        generate_dir(path.path, out, context=_context)

    if path.is_single:
        if os.path.isdir(out):
            out = os.path.join(out, path.path)
        generate(path.path, out, context=_context)

    click.secho("Generate success ~ !!", fg='green')


if __name__ == '__main__':
    cli()
