import pytest

from pdchaoskit.settings import set_settings, get_api_url, get_api_token, \
    update_settings_from_env, ensure_settings_are_valid, add_to_run_context, no_upload


def test_set_settings():
    # arrange
    settings = {}
    api_url = "https://chaosapi.proofdock.io"
    api_token = (
        "eyJ0eXAiOiJKV1QiLCJhbGcddiJIUzI1NiJ9"
        ".eyJpc3MiOiI1MzAwMTA5OC00MDNkLTY4NjMt"
        "OTdlNS1jMjJlYzNiNmE3NzciLCJpYXQiOjE1Nz"
        "k4MDkzMDAsImV4cCI6MTU5NTM1NzcwMCwiYXVk"
        "IjoibG9jYWwuY2hhb3MuYXBpIiwic3ViIjoiMj"
        "hjMTBlM2QtNjI2ZS00OTNhLThmMjYtOWFiOTk0"
        "MjczNzAxIiwic2NwIjoiNzJhZTQ0MTMtNzQwYS"
        "00ZTc0LTk5ZmQtMmRhNzI5YWQ4MzkxIn0.r_2q"
        "P0NH0AcdUL7v1VZgJs2v6R13zWXA1KqiUPalbo4")

    # act
    settings = set_settings(settings, api_url, api_token)

    # assert
    control = settings.get('controls').get('proofdock', None)
    provider = control.get('provider', None)
    auth = settings.get('auths').get('chaosapi.proofdock.io', None)
    assert control is not None
    assert provider is not None
    assert provider.get('module') == 'pdchaoskit.controls'
    assert provider.get('type') == 'python'
    assert provider.get('arguments').get('api_url') == \
        'https://chaosapi.proofdock.io'
    assert auth is not None
    assert auth.get('type') == 'bearer'
    assert auth.get('value') == api_token


def test_set_settings_without_token():
    # arrange
    settings = {}
    api_url = "https://chaosapi.proofdock.io"
    api_token = None

    # act
    settings = set_settings(settings, api_url, api_token)

    # assert
    control = settings.get('controls').get('proofdock', None)
    auth = settings.get('auths', {}).get('chaosapi.proofdock.io', None)
    provider = control.get('provider', None)
    assert control is not None
    assert provider is not None
    assert provider.get('module') == 'pdchaoskit.controls'
    assert provider.get('type') == 'python'
    assert provider.get('arguments').get('api_url') == \
        'https://chaosapi.proofdock.io'
    assert auth is None


def test_get_api_url():
    # arrange
    settings = {
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                    'arguments': {
                        'api_url': "https://some.api.io"
                    }
                }
            }
        }
    }
    # act & assert
    assert get_api_url(settings) == "https://some.api.io"


def test_get_api_url_from_env(monkeypatch):
    # arrange
    settings = {
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                }
            }
        }
    }

    monkeypatch.setenv("PROOFDOCK_API_URL", "https://api.from.env.io")

    # act
    update_settings_from_env(settings)

    # assert
    arguments = settings['controls']['proofdock']['provider']\
        .get('arguments', None)
    assert arguments is not None
    assert arguments.get('api_url') == "https://api.from.env.io"
    assert get_api_url(settings) == "https://api.from.env.io"


def test_override_api_url_from_env(monkeypatch):
    # arrange
    settings = {
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }

    monkeypatch.setenv("PROOFDOCK_API_URL", "https://api.from.env.io")

    # act
    update_settings_from_env(settings)

    # assert
    arguments = settings['controls']['proofdock']['provider']\
        .get('arguments', None)
    assert arguments is not None
    assert arguments.get('api_url') == "https://api.from.env.io"
    assert get_api_url(settings) == "https://api.from.env.io"


def test_get_api_token():
    # arrange
    settings = {
        'auths': {
            'proofdock.io': {
                'value': "my.token"
            }
        }
    }

    # act & assert
    assert get_api_token(settings, "https://proofdock.io") == "my.token"


def test_set_api_token_from_env(monkeypatch):
    # arrange
    settings = {
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }
    monkeypatch.setenv("PROOFDOCK_API_TOKEN", "my.token.from.env")

    # act
    update_settings_from_env(settings)

    # assert
    assert settings['auths']['chaosapi.proofdock.io']['value'] == \
        "my.token.from.env"
    assert get_api_token(settings) == "my.token.from.env"


def test_override_api_token_from_env(monkeypatch):
    # arrange
    settings = {
        'auths': {
            'chaosapi.proofdock.io': {
                'value': 'token.from.settings'
            }
        },
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }

    monkeypatch.setenv("PROOFDOCK_API_TOKEN", "my.token.from.env")

    # act
    update_settings_from_env(settings)

    # assert
    assert settings['auths']['chaosapi.proofdock.io']['value'] == \
        "my.token.from.env"
    assert get_api_token(settings) == "my.token.from.env"


def test_ensure_settings_are_valid():
    # arrange
    settings = {
        'auths': {
            'chaosapi.proofdock.io': {
                'value': 'token.from.settings'
            }
        },
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }

    # act
    ensure_settings_are_valid(settings)


def test_ensure_settings_are_valid_missing_auths():
    # arrange
    settings = {
        'auths': {
        },
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                    'arguments': {
                        'api_url': 'https://chaosapi.proofdock.io/'
                    }
                }
            }
        }
    }

    # act
    with pytest.raises(Exception):
        ensure_settings_are_valid(settings)


def test_ensure_settings_are_valid_missing_api_url():
    # arrange
    settings = {
        'auths': {
            'chaosapi.proofdock.io': {
                'value': 'token.from.settings'
            }
        },
        'controls': {
            'proofdock': {
                'provider': {
                    'module': 'pdchaoskit.controls',
                    'type': 'python',
                    'arguments': {}
                }
            }
        }
    }

    # act
    with pytest.raises(Exception):
        ensure_settings_are_valid(settings)


def test_ensure_settings_are_valid_missing_control():
    # arrange
    settings = {
        'auths': {
            'chaosapi.proofdock.io': {
                'value': 'token.from.settings'
            }
        }
    }

    # act
    with pytest.raises(Exception):
        ensure_settings_are_valid(settings)


def test_add_to_run_context():
    # arrange
    settings = {}

    # act
    settings = add_to_run_context(settings, 'key', 'value')

    # assert
    assert settings.get('run_context')['key'] == 'value'


def test_no_upload_enabled():
    # arrange
    settings = {
        'run_context': {
            'no_upload': True
        }
    }

    # act & assert
    assert no_upload(settings) is True


def test_no_upload_disabled():
    # arrange
    settings = {
        'run_context': { }
    }

    # act & assert
    assert no_upload(settings) is False
