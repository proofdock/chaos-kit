# Proofdock extension for the Chaos Toolkit

[![Build Status](https://dev.azure.com/proofdockio/chaos/_apis/build/status/chaos-kit/chaos-kit%20-%20production?branchName=master)](https://dev.azure.com/proofdockio/chaos/_build/latest?definitionId=58&branchName=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-kit.svg)](https://www.python.org/)

This project is a collection of features gathered as an extension to the [Proofdock Chaos Engineering Platform][chaosengineeringplatform] and the [Chaos Toolkit][chaostoolkit].


## Project description

This project is part of the Proofdock Chaos Engineering Platform that helps you to write, run, store and analyze chaos experiments in your Azure DevOps environment.

For more information visit our official [website][proofdock] or [documentation][proofdock_docs]. Feel free to ask for support for this package on [GitHub][proofdock_support].



## Install

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-kit
```

## Usage

To use the features ...

## Configuration

This extension uses ...

### Putting it all together

Here is a full example for

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Proofdock projects require all contributors to sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```

[chaosengineeringplatform]: https://proofdock.io
[chaostoolkit]: https://chaostoolkit.org
[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/