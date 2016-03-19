#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
        'agen=agen:cli'
    ]
}

requirements = [
    'jinja2',
    'click',
    'PyYaml',
    'six',
    'chardet'
]

test_requirements = [
    'pytest'
]

setup(
    name='agen',
    version='0.1.1',
    description="A very simple code generator.",
    author="Yufei Li",
    author_email='yufeiminds@163.com',
    url='https://github.com/yufeiminds/agen',
    py_modules=['agen'],
    entry_points=entry_points,
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='agen',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
