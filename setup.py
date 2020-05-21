#!/usr/bin/env python
"""The Proofdock chaos-kit extension for the Chaos Engineering Platform"""

import os
import sys

import setuptools


def get_version_from_package() -> str:
    """
    Read the package version from the source without importing it.
    """

    path = os.path.join(os.path.dirname(__file__), "pdchaoskit/__init__.py")
    path = os.path.normpath(os.path.abspath(path))
    with open(path) as f:
        for line in f:
            if line.startswith("__version__"):
                token, version = line.split(" = ", 1)
                version = version.replace("'", "").strip()
                print(version)
                return version


def get_requirements(filename):
    """Get requirements from a requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


name = 'proofdock-chaos-kit'
version = get_version_from_package()
url = 'https://proofdock.io'
desc = 'Extend the Chaos Toolkit with capabilities for the Proofdock Chaos Engineering Platform'
with open("README.md", "r") as fh:
    long_description = fh.read()
author = 'Proofdock'
author_email = 'hello@proofdock.io'
license = 'Apache License Version 2.0'
packages = [
    'pdchaoskit',
    'pdchaoskit.api'
]

classifiers = [
    'Intended Audience :: Developers',
    'License :: Freely Distributable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: Implementation :: CPython'
]
project_urls = {
    "Documentation": "https://docs.proofdock.io/",
    "Support": "https://github.com/proofdock/chaos-support"
}


needs_pytest = set(['pytest', 'test']).intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []

if __name__ == "__main__":
    setuptools.setup(
        name=name,
        version=version,
        description=desc,
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=classifiers,
        project_urls=project_urls,
        author=author,
        author_email=author_email,
        url=url,
        license=license,
        packages=packages,
        install_requires=get_requirements("requirements.txt"),
        tests_require=get_requirements("requirements-dev.txt"),
        setup_requires=pytest_runner,
        include_package_data=True,
        python_requires='>=3.5.*',
        entry_points={
            'chaostoolkit.cli_plugins': [
                'configure = pdchaoskit.cli:configure',
                'experiment = pdchaoskit.cli:experiment',
            ]
        }

    )
