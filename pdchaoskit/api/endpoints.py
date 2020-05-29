from urllib import parse
from chaoslib.settings import get_loaded_settings
from pdchaoskit.settings import get_api_url


def base():
    return get_api_url(get_loaded_settings())


def events():
    return _get_url(base(), 'v1/events')


def executions():
    return _get_url(base(), 'v1/executions')


def experiment():
    return _get_url(base(), 'v1/experiments')


def scripts():
    return _get_url(base(), 'v1/scripts')


def _get_url(base: str, address: str):
    base = base if base.endswith("/") else base + "/"
    return parse.urljoin(base, address)
