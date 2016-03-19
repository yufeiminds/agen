agen
=======

A very simple code generator.

.. image:: https://img.shields.io/pypi/v/agen.svg
   :target: https://pypi.python.org/pypi/agen/
   :alt: Latest Version
.. image:: https://travis-ci.org/yufeiminds/agen.svg?branch=master
   :target: https://travis-ci.org/yufeiminds/agen
   :alt: Travis CI Status
.. image:: https://codecov.io/github/yufeiminds/agen/coverage.svg?branch=master
   :target: https://codecov.io/github/yufeiminds/agen?branch=master
   :alt: Codecov Status
.. image:: https://readthedocs.org/projects/agen/badge/?version=latest
   :target: http://agen.readthedocs.org/en/latest/?badge=latest
   :alt: Doc Status

-  Free software: MIT license
-  Documentation: https://agen.readthedocs.com/en/ .

Features
--------

-  Simple and very simple API
-  Custom ``Jinja Env`` supported
-  Could be used as Command-Line-Tools

**No Template**

*agen* don't provide any template. It's only provide some function,
to make code to be a template. If you need any public template, please
use the awesome open source tool,
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ .

**Why agen?**

agen is so lightweight, that could be perfectly integrated into your
project in minutes.

I like `Cookiecutter <https://github.com/audreyr/cookiecutter>`__ (It's
so cool and so awesome), but most of it's features are too heavyweight
for me.

Installation
------------

Install with pip:

.. code:: shell

    pip install agen

Install with source code:

.. code:: shell

    clone https://github.com/yufeiminds/agen.git
    cd agen
    python setup.py install

Quickstart Guide
----------------

In *agen*, use `jinja2 <http://jinja.pocoo.org/docs/>`__ as
template engine for rendering, so, any feature of
`jinja2 <http://jinja.pocoo.org/docs/>`__ template will be found in
*agen* .

File Generation
~~~~~~~~~~~~~~~

.. code-block:: python

    from agen import (
        string_render,
        render,
        generate,
        generate_dir
    )

    # Render text from a templated string
    string_render('{{key}}', {'key': 'value'})
    > 'value'

    cat template.py
    > {{key}}

    # Render text from a template file
    render('template.py', {'key': 'value'})
    > 'value'

    # Generate file from a template file
    generate('template.py', 'output.py', {'key': 'value'})

    # Content of output.py
    value

Directory Generation
~~~~~~~~~~~~~~~~~~~~

If we have a directory like this：

.. code:: shell

    directory
    ├── __init__.py
    └── {{key}}.py

call ``generate_dir`` function：

.. code-block:: python

    generate_dir('directory', 'mydir', {'key': 'value'})

will generate

.. code:: shell

    mydir
    ├── __init__.py
    └── value.py

Every pure text file will be render by template engine. **context**
``{'key': 'value'}`` also will be rendered automatically.

Command Line Tool
-----------------

Basic Usage
~~~~~~~~~~~

*agen* also implement a very simple command line tool, use for
rendering the local template easily, but it only could be used on \*UNIX
operation system.

::

    Usage: agen [OPTIONS] [NAMES]...

    Options:
      -o, --out PATH      Output path or directory
      -s, --source PATH   Source path or directory
      -c, --context PATH  Path of context file
      --help              Show this message and exit.

With no argument，\ *agen* will search local template directory, eg.
on \*NIX operation system, this directory are usually at:

::

    $ agen
    --------------------------------------------
      agen Library
      see -> /Users/yufeili/.agen/templates
    --------------------------------------------
    directory   repo        single.txt

The simplest way to call：

::

    $ agen -s template_path -o ouput_path -c context.json

Sure, ``.yaml`` also can be used as ``context`` file. If the ``out``
option wasn't provided, it will prompt for input on screen (defualt is
current directory).

Full Example
~~~~~~~~~~~~

You can specific three kinds of directory or file as the ``source`` .

Single File
^^^^^^^^^^^

::

    $ agen -s single.txt -o output.txt -c context.json

Directory
^^^^^^^^^

Any directory, such as

::

    directory
    ├── __init__.py
    └── {{key}}.py

both could be ``source``, it also support to use template variable to
render the output file name.

::

    $ agen -s directory -o myapp -c context.json

This command will create a directory named ``myapp``, and processing
recursively all files under the ``directory`` , output to ``myapp`` base
on origin structure.

Repository
^^^^^^^^^^

.. Note:: agen is not designed as a command line tool, so for generating repository, recommend to use the awesome `Cookiecutter <https://github.com/audreyr/cookiecutter>`__ .

If there is an inner folder in a directory, and the directory has a
``agen.json`` or ``agen.yaml`` , it will be judged as a
``Repo``\ ，

::

    repo
    ├── README.md
    ├── agen.json
    └── {{name}}
        ├── __init__.py
        └── {{name}}.py

The default behavior of this tool will be changed, assuming this
**Repo**

::

    $ agen -s repo -o output -c context.json

-  This command will create a folder has the same name with inner
   directory to ``output`` directory, if the name of folder is a
   template string, it will be compiled as standard string then create a
   folder, the other behavior same as ``directory`` .
-  The ``context`` is not required. If it wasn't provided, it will load
   the ``agen.[json|yaml]`` file, and prompt user for input.

Example
^^^^^^^

For **context** ``{'key': 'value'}``，**output** is current
directory, current value:

::

    .
    └── value
        ├── __init__.py
        └── value.py

Local Template Directory
''''''''''''''''''''''''

Use option argument ``NAMES``, could get files path from local templates
directory as ``source`` . The following two calls are equivalent in
\*NIX systems:

::

    $ agen -s ~/.agen/templates/single.txt
    $ agen single.txt

Credits
-------

-  Author : Yufei Li yufeiminds@gmail.com
-  Contact me: @yufeiminds (Facebook)、@YufeiMinds (Sina Weibo)

Contribution
------------

Welcome to develop with me!

Fork this repo & develop it.

