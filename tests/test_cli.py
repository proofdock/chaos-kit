from pdchaoskit.cli import cli
from click.testing import CliRunner
from unittest.mock import ANY, patch


@patch('pdchaoskit.cli.save_settings', spec=True)
@patch('pdchaoskit.cli.load_settings', spec=True)
def test_configure(load_settings, save_settings):
    # arrange
    load_settings.return_value = {}
    runner = CliRunner()

    # act
    result = runner.invoke(cli, [
        '--settings', '/home/settings.yaml', 'configure'])

    # assert
    assert result.exit_code == 0
    load_settings.assert_called_once_with('/home/settings.yaml')
    save_settings.assert_called_once_with(ANY, '/home/settings.yaml')
    (args, kwargs) = save_settings.call_args
    assert args[0] == {
        'controls': {
            'proofdock': {
                'provider': {
                    'type': 'python',
                    'module': 'pdchaoskit.controls',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }
    assert args[1] == '/home/settings.yaml'


@patch('pdchaoskit.cli.save_settings', spec=True)
@patch('pdchaoskit.cli.load_settings', spec=True)
def test_configure_with_token(load_settings, save_settings):
    # arrange
    load_settings.return_value = {}
    runner = CliRunner()

    # act
    result = runner.invoke(cli, [
        '--settings', '/home/settings.yaml', 'configure', '--token', 'my.super.token'])

    # assert
    assert result.exit_code == 0
    load_settings.assert_called_once_with('/home/settings.yaml')
    save_settings.assert_called_once_with(ANY, '/home/settings.yaml')
    (args, kwargs) = save_settings.call_args
    assert args[0] == {
        'auths': {
            'chaosapi.proofdock.io': {
                'type': 'bearer',
                'value': 'my.super.token'
            }
        },
        'controls': {
            'proofdock': {
                'provider': {
                    'type': 'python',
                    'module': 'pdchaoskit.controls',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }
    assert args[1] == '/home/settings.yaml'


@patch('pdchaoskit.cli.save_settings', spec=True)
@patch('pdchaoskit.cli.load_settings', spec=True)
def test_configure_renew_token(load_settings, save_settings):
    # arrange
    load_settings.return_value = {
        'auths': {
            'chaosapi.proofdock.io': {
                'type': 'bearer',
                'value': 'my.super.token'
            }
        },
        'controls': {
            'proofdock': {
                'provider': {
                    'type': 'python',
                    'module': 'pdchaoskit.controls',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }
    runner = CliRunner()

    # act
    result = runner.invoke(cli, [
        '--settings', '/home/settings.yaml', 'configure', '--token', 'renewed.token'])

    # assert
    assert result.exit_code == 0
    load_settings.assert_called_once_with('/home/settings.yaml')
    save_settings.assert_called_once_with(ANY, '/home/settings.yaml')
    (args, kwargs) = save_settings.call_args
    assert args[0] == {
        'auths': {
            'chaosapi.proofdock.io': {
                'type': 'bearer',
                'value': 'renewed.token'
            }
        },
        'controls': {
            'proofdock': {
                'provider': {
                    'type': 'python',
                    'module': 'pdchaoskit.controls',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }
    assert args[1] == '/home/settings.yaml'


@patch('pdchaoskit.cli.save_settings', spec=True)
@patch('pdchaoskit.cli.load_settings', spec=True)
def test_configure_default_api_url(load_settings, save_settings):
    # arrange
    load_settings.return_value = {}
    runner = CliRunner()

    # act
    result = runner.invoke(cli, [
        '--settings', '/home/settings.yaml', 'configure', '--default-api-url', 'https://new.api.io/'])

    # assert
    assert result.exit_code == 0
    load_settings.assert_called_once_with('/home/settings.yaml')
    save_settings.assert_called_once_with(ANY, '/home/settings.yaml')
    (args, kwargs) = save_settings.call_args
    assert args[0] == {
        'controls': {
            'proofdock': {
                'provider': {
                    'type': 'python',
                    'module': 'pdchaoskit.controls',
                    'arguments': {
                        'api_url': 'https://new.api.io/'
                    }
                }
            }
        }
    }
    assert args[1] == '/home/settings.yaml'


@patch('pdchaoskit.cli.save_settings', spec=True)
@patch('pdchaoskit.cli.load_settings', spec=True)
def test_configure_override_default_api_url(load_settings, save_settings):
    # arrange
    load_settings.return_value = {
        'controls': {
            'proofdock': {
                'provider': {
                    'type': 'python',
                    'module': 'pdchaoskit.controls',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }
    runner = CliRunner()

    # act
    result = runner.invoke(cli, [
        '--settings', '/home/settings.yaml', 'configure', '--default-api-url', 'https://new.api.io/'])

    # assert
    assert result.exit_code == 0
    load_settings.assert_called_once_with('/home/settings.yaml')
    save_settings.assert_called_once_with(ANY, '/home/settings.yaml')
    (args, kwargs) = save_settings.call_args
    assert args[0] == {
        'controls': {
            'proofdock': {
                'provider': {
                    'type': 'python',
                    'module': 'pdchaoskit.controls',
                    'arguments': {
                        'api_url': 'https://new.api.io/'
                    }
                }
            }
        }
    }
    assert args[1] == '/home/settings.yaml'
