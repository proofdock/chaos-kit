import os
from urllib.parse import urlparse

from chaoslib.types import Control, Settings

DEFAULT_PROOFDOCK_API_URL = 'https://chaosapi.proofdock.io/'


def get_api_url(settings: Settings) -> str:
    """Get the Proofdock API endpoint.
    """
    return _get_control(settings) \
        .get('provider', {}).get('arguments', {}) \
        .get('api_url', '')


def get_api_token(settings: Settings, url: str = DEFAULT_PROOFDOCK_API_URL) \
        -> str:
    """Get the token for the Proofdock API endpoint.
    """
    return settings.get('auths', {}).get(urlparse(url).netloc, {}).get('value', '')


def set_settings(settings: Settings, api_url: str, token: str):
    if token:
        _set_auth(settings, api_url, token)
    control = _get_control(settings)
    control.update({
        'provider': {
            'type': 'python',
            'module': 'pdchaoskit.controls',
        }
    })
    if api_url:
        control.get('provider').update({
            'arguments': {
                'api_url': api_url
            }
        })
    return settings


def update_settings_from_env(settings: Settings):
    api_url = _get_variable_or_default('PROOFDOCK_API_URL', get_api_url(settings)) or DEFAULT_PROOFDOCK_API_URL
    api_token = _get_variable_or_default('PROOFDOCK_API_TOKEN', None)
    return set_settings(settings, api_url, api_token)


def ensure_settings_are_valid(settings: Settings):
    """
    Check if settings include all required entries that are required by the Proofdock extension
    """
    if not _get_control(settings):
        raise Exception(
            '\n'
            'Proofdock Chaos Kit is not configured.')

    api_url = get_api_url(settings)
    if not api_url:
        raise Exception(
            '\n'
            'Proofdock Cloud URL is not set. '
            'Please set it first by calling:\n\n'
            '$ chaos configure --default-api-url <API_URL>\n'
            'or set PROOFDOCK_API_URL environment variable.')

    if not get_api_token(settings, api_url):
        raise Exception(
            '\n'
            'Proofdock Cloud API Token is not set. '
            'Please set it first by calling:\n\n'
            '$ chaos configure --token <API_TOKEN>\n\n'
            'or set PROOFDOCK_API_TOKEN environment variable.')

    return True


def add_to_run_context(settings, key, value):
    """
    Add key and value carefully to the settings
    :param key: the key to be added
    :param value: the value belonging to the key
    :param settings: the loaded settings
    :return:
    """
    if 'run_context' not in settings:
        settings['run_context'] = {}

    settings['run_context'][key] = value
    return settings


def _set_auth(settings: Settings, api_url: str, token: str):
    if 'auths' not in settings:
        settings['auths'] = {}

    p = urlparse(api_url)
    for domain in settings['auths']:
        if domain == p.netloc:
            auth = settings['auths'][domain]
            auth["type"] = "bearer"
            auth["value"] = token
            break
    else:
        auth = settings['auths'][p.netloc] = {}
        auth["type"] = "bearer"
        auth["value"] = token


def _get_control(settings: Settings) -> Control:
    controls = settings.setdefault('controls', {})
    return controls.setdefault('proofdock', {})


def _get_variable_or_default(var: str, default: str):
    if var in os.environ and os.environ[var]:
        return os.environ[var]
    else:
        return default
