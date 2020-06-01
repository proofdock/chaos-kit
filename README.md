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

The Proofdock Chaos CLI extends the [Chaos Toolkit][chaostoolkit]. The several Proofdock Chaos CLI commands are explained in detail at the [Proofdock documentation homepage][proofdock_docs_chaoscli].

## Configuration

The Proofdock Chaos CLI expects that you have an API url and a proper API token that allows you to authenticate against the Proofdock cloud.

Configuration values for the Proofdock Chaos CLI can come from several sources:

* Settings file, e.g.
  ```yaml
  # located in ~/.chaostoolkit/settings.yaml
  auths:
    chaosapi.proofdock.io:
      type: bearer
      value: <your_api_token_here>
  controls:
    proofdock:
      provider:
        arguments:
          api_url: https://chaosapi.proofdock.io/
        module: pdchaoskit.controls
        type: python
  ```
* You may override the settings file with the environment variable ``PROOFDOCK_API_TOKEN`` which overrides the token from your settings file.

The Proofdock Chaos CLI will first try to load the configuration from the settings file. If no configuration is provided, it will try to load it from the environment variables. Please check the [usage command][proofdock_chaoskit_configure] to see how to set up the settings file with the Proofdock Chaos CLI.

### Putting it all together

Here is a full example to configure the Chaos CLI, run an experiment and list those experiments.

1. Configure the settings file with the API token that you have gathered from the Proofdock Chaos Engineering Platform.
   ```bash
   chaos configure --token <your-api-token>
   ```
   More configuration options are vailable. For more options check out the CLI ``--help`` command itself or have a look at the [docs][proofdock_chaoskit_configure].


2. Run an experiment and send its results to the Proofdock cloud.
    ```bash
    chaos run /path/to/experiment.yml
    ```
   You may use several options like providing descriptions to your experiment run. For more options check out the CLI ``--help`` command itself or have a look at the [docs][proofdock_chaoskit_run].


3. Retrieve and list experiments from the Proofdock cloud.
    ```bash
    chaos experiment list
    ```
    For more options check out the CLI ``--help`` command itself or have a look at the [docs][proofdock_chaoskit_list].


You have now configured your Chaos CLI and successfully run an experiment.


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
[proofdock_chaoskit_configure]:[https://docs.proofdock.io/chaos/cli/configure/]
[proofdock_chaoskit_run]:[https://docs.proofdock.io/chaos/cli/run/]
[proofdock_chaoskit_list]:[https://docs.proofdock.io/chaos/cli/list/]
[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_docs_chaoscli]: https://docs.proofdock.io/chaos/cli
[proofdock_support]: https://github.com/proofdock/chaos-support/