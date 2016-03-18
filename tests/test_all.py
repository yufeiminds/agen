# coding=utf8

"""
Copyright 2016 Yufei Li
"""

import os
import pytest
import textgen
from click.testing import CliRunner

single = os.path.join('tests', 'templates', 'single.txt')
repo = os.path.join('tests', 'templates', 'repo')
directory = os.path.join('tests', 'templates', 'directory')
ctx_json = os.path.join('tests', 'context', 'demo.json')
ctx_yaml = os.path.join('tests', 'context', 'demo.yaml')


@pytest.fixture(autouse=True)
def runner():
    return CliRunner()


def assert_content(file_path, content):
    with open(file_path) as f:
        assert f.read() == content


def test_string_render():
    result = textgen.string_render("{{name}}", context={"name": "demo"})
    assert result == "demo"


def test_abs_render():
    assert textgen.render(single, context={"name": "demo"}) == "demo"


def test_single_file(tmpdir):
    out = os.path.join(tmpdir.strpath, 'single.txt')
    textgen.generate(single, out, context={"name": "demo"})
    assert_content(out, "demo")


def test_directory(tmpdir):
    out = os.path.join(tmpdir.strpath, 'demo')
    textgen.generate_dir(directory, out, context={"name": "demo"})
    assert os.path.exists(out)
    assert os.path.exists(os.path.join(out, "demo.py"))
    assert_content(os.path.join(out, "__init__.py"), "demo")


def test_repo(tmpdir):
    out = tmpdir.strpath
    path = textgen.Path(repo)
    context = {
        "name": "repo"
    }
    inner = path.inner
    out_name = textgen.string_render(os.path.split(inner)[-1], context)
    out = os.path.join(out, out_name)
    textgen.generate_dir(inner, out, context)
    assert os.path.exists(out)
    assert os.path.exists(os.path.join(out, out_name + ".py"))
    assert_content(os.path.join(out, "__init__.py"), "repo")


def test_path_checker():
    path = textgen.Path(single)
    assert path.is_single
    path = textgen.Path(repo)
    assert path.is_repo
    path = textgen.Path(directory)
    assert path.is_dir


def test_cli_single(tmpdir, runner):
    out = os.path.join(tmpdir.strpath, 'single.txt')
    runner.invoke(textgen.cli, ['-s', single, '-o', out, '-c', ctx_json])
    assert_content(out, "demo")


def test_cli_directory(tmpdir, runner):
    out = os.path.join(tmpdir.strpath, 'demo')
    result = runner.invoke(textgen.cli,
                           ['-s', directory, '-o', out, '-c', ctx_json])
    assert result.exit_code == 0
    assert os.path.exists(out)
    assert os.path.exists(os.path.join(out, "demo.py"))
    assert_content(os.path.join(out, "__init__.py"), "demo")


def test_cli_repo(tmpdir, runner):
    out = tmpdir.strpath
    result = runner.invoke(textgen.cli,
                           ['-s', repo, '-o', out, '-c', ctx_json])
    assert result.exit_code == 0
    assert os.path.exists(out)
    assert os.path.exists(os.path.join(out, "demo", "demo.py"))
    assert_content(os.path.join(out, "demo", "__init__.py"), "demo")


def test_cli_repo_prompt(tmpdir, runner):
    out = tmpdir.strpath
    result = runner.invoke(textgen.cli, ['-s', repo, '-o', out],
                           input="repo\n")
    assert result.exit_code == 0
    assert os.path.exists(out)
    assert os.path.exists(os.path.join(out, "repo", "repo.py"))
    assert_content(os.path.join(out, "repo", "__init__.py"), "repo")


def test_cli_path_not_existed(tmpdir, runner):
    result = runner.invoke(textgen.cli,
                           ['-o', tmpdir.strpath, '_test/a'])
    assert "does not exist" in result.output
    result = runner.invoke(textgen.cli,
                           ['-s', '_test/a', '-o', tmpdir.strpath])
    assert "does not exist" in result.output


def test_cli_prompt_app_folder(tmpdir, runner):
    import subprocess

    _folder = textgen.app_folder
    _check_call = subprocess.check_call

    textgen.app_folder = tmpdir.strpath

    def check_call(*args, **kwargs):
        return None

    subprocess.check_call = check_call
    result = runner.invoke(textgen.cli, [])
    assert result.exit_code == 0
    assert "Library" in result.output

    textgen.app_folder = _folder
    subprocess.check_call = _check_call


def test_cli_input_oudir(tmpdir, runner):
    result = runner.invoke(textgen.cli, ['-s', single, '-c', ctx_yaml],
                           input=tmpdir.strpath)
    assert result.exit_code == 0
    assert "Output directory" in result.output
