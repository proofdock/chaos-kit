# Proofdock extension for the Chaos Toolkit

[![Build Status](https://dev.azure.com/proofdockio/chaos/_apis/build/status/chaos-kit/chaos-kit%20-%20production?branchName=master)](https://dev.azure.com/proofdockio/chaos/_build/latest?definitionId=58&branchName=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-kit.svg)](https://www.python.org/)

This project is a collection of features gathered as an extension to the [Proofdock Chaos Engineering Platform][chaosengineeringplatform] and the [Chaos Toolkit][chaostoolkit].


## Project description

This project is part of the Proofdock Chaos Engineering Platform that helps you to write, run, store and analyze chaos experiments in your Azure DevOps environment.

For more information visit our official [website][proofdock] or [documentation][proofdock_docs]. Feel free to ask for support for this package on [GitHub][proofdock_support].

## Getting started

To get started check out our official [guide][proofdock_docs_get_started].


## Install

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-kit
```

## Configuration

The Proofdock Chaos CLI expects that you have a proper API token that allows you to authenticate against the Proofdock cloud. Learn more about the API token generation [here][proofdock_docs_project_settings].

To configure the API token you simply pass it to the ``chaos configure`` command.  

``` bash
chaos configure --token <API token>
```
Chaos CLI stores your API token in a settings file located under the following path:

``` bash
$HOME/.chaostoolkit/settings.yaml
```

Alternatively set the API token using an environment variable ``PROOFDOCK_API_TOKEN``.

``` bash
export PROOFDOCK_API_TOKEN=<API token>
```

**Precedence of options**

If you specify the API token by using the `PROOFDOCK_API_TOKEN` environment variable, it overrides any API token value loaded from a settings file.


## Commands

The Proofdock Chaos CLI introduces new commands:
- `chaos configure`
- `chaos experiment`

and extends an existing `chaos run` command with new options.

### Run
You use the `chaos run` command to run an experiment and upload its results to the Proofdock cloud.

``` bash
chaos run [OPTIONS] experiment.json
```

### Configure
You use the `chaos configure` command to set the API token in a settings file.

``` bash
chaos configure --token <API token>
```

**Options**
``` bash
  --token TEXT            Token value
```

### List
You use ``experiment list`` command to list all experiments in your project.

``` bash
chaos experiment list
```

[chaosengineeringplatform]: https://proofdock.io
[chaostoolkit]: https://chaostoolkit.org
[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_docs_get_started]: https://docs.proofdock.io/chaos/guide
[proofdock_docs_project_settings]: https://docs.proofdock.io/chaos/devops/settings/#project-settings
[proofdock_support]: https://github.com/proofdock/chaos-support/
