.. raw:: html

   <div class="indexwrapper">
    <h1>
        Agen
        <a class="headerlink" href="#agen" title="Permalink to this headline">¶</a>
    </h1>
   </div>

一个极简的代码生成器，可以嵌进你自己的项目中。

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

-  自由软件: MIT license
-  English Documentation: https://agen.readthedocs.com/en/

特性
----

-  简化到不能再简化的API
-  支持自定义 ``Jinja Env``
-  可以作为命令行工具使用

**无模版**

*agen*
本身并不提供任何代码模版，只是提供一种能力，将代码模版化。如果需要使用已有的公开模版，请通过另一个优秀的开源库
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ 。

**为什么?**

agen 十分轻量级，可以在几分钟内完美集成到你自己的项目中。

我非常喜爱 `Cookiecutter <https://github.com/audreyr/cookiecutter>`__
这个非常酷的项目，但它的绝大多数功能对我来说太重了。

安装
----

使用 pip 安装：

::

    pip install agen

从源代码安装：

.. code:: shell

    clone https://github.com/yufeiminds/agen.git
    cd agen
    python setup.py install

快速指南
--------

在 *agen* 中，使用
`jinja2 <http://jinja.pocoo.org/docs/>`__ 作为模版引擎进行渲染，所以，任何
`jinja2 <http://jinja.pocoo.org/docs/>`__
模版的特性都可以在agen中使用。

文件生成
~~~~~~~~

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

目录生成
~~~~~~~~

假设我们有下面这样的目录：

.. code:: shell

    directory
    ├── __init__.py
    └── {{key}}.py

调用 ``generate_dir`` 函数：

.. code-block:: python

    generate_dir('directory', 'mydir', {'key': 'value'})

将生成

.. code:: shell

    mydir
    ├── __init__.py
    └── value.py

每一个纯文本文件都会被模版引擎渲染，\ **context** ``{'key': 'value'}``
也会在渲染时被自动传递。

命令行工具
----------

基本用法
~~~~~~~~

*agen*
也实现了一个非常简单的命令行工具，用于快速渲染本地的模版，但只能用于\*NIX系统。

::

    Usage: agen [OPTIONS] [NAMES]...

    Options:
      -o, --out PATH      Output path or directory
      -s, --source PATH   Source path or directory
      -c, --context PATH  Path of context file
      --help              Show this message and exit.

不带参数时，\ *agen* 会搜索本地的模版目录，eg.
在\*NIX系统上，这个目录通常是

::

    $ agen
    --------------------------------------------
      agen Library
      see -> /Users/yufeili/.agen/templates
    --------------------------------------------
    directory   repo        single.txt

最简单的调用方法是：

::

    $ agen -s template_path -o ouput_path -c context.json

当然，\ ``.yaml`` 文件也是可以作为 ``context``
使用的。如果不提供\ ``out`` 选项，会有输入提示（默认为当前目录）。

完整示例
~~~~~~~~

可以指定三种目录或者文件作为 ``源目录`` 。

单文件
^^^^^^

::

    $ agen -s single.txt -o output.txt -c context.json

目录
^^^^

任何目录，比如

::

    directory
    ├── __init__.py
    └── {{key}}.py

都可以作为源路径，当然也支持用模版变量来输出文件名。

::

    $ agen -s directory -o myapp -c context.json

这条命令会创建一个名字叫 ``myapp`` 的目录，将 ``directory``
下所有的文件都递归地处理，同时按原来的结构输出到 ``myapp`` 中。

Repository
^^^^^^^^^^

.. note:: agen 并非是作为一个命令行工具来设计的，对于repository的命令行生成，建议使用更加优秀的开源工具 `Cookiecutter <https://github.com/audreyr/cookiecutter>`__

如果一个目录里面有一个内部文件夹，同时还有一个 ``agen.json`` 或者
``agen.yaml``\ ，那么会判定这个文件夹是一个\ ``Repo``\ ，

::

    repo
    ├── README.md
    ├── agen.json
    └── {{name}}
        ├── __init__.py
        └── {{name}}.py

此时工具的默认行为会改变，假设对于上面的 **Repo**

::

    $ agen -s repo -o output -c context.json

-  这条命令会在 ``output``
   目录下建立一个与内部文件夹同名的文件夹，如果是文件夹的名字是模版字符串，会编译成标准字符串后再建立文件夹，其它的行为与标准目录相同。
-  此时 *context* 路径不是必需的，如果不提供，会读取 **Repo** 源目录里的
   ``agen.[json|yaml]`` ，并提示用户交互式地输入。

示例
^^^^

对于 **context** ``{'key': 'value'}`` ，**output**
是当前目录的情况下，会在当前目录下产生：

::

    .
    └── value
        ├── __init__.py
        └── value.py

本地模版目录
^^^^^^^^^^^^

使用可选参数``NAMES``，会将本地模版目录下的文件指定为源路径，以下两种调用方式在\*NIX系统中是等价的：

::

    $ agen -s ~/.agen/templates/single.txt
    $ agen single.txt

关于
----

-  Author : Yufei Li yufeiminds@gmail.com
-  Contact me: @yufeiminds (Facebook)、@YufeiMinds (Sina Weibo)

贡献
----

欢迎与我一起开发!

Fork this repo & develop it.
