from urllib import parse
from chaoslib.settings import get_loaded_settings
from pdchaoskit.settings import get_api_url


def base() -> str:
    return get_api_url(get_loaded_settings())


def alerts() -> str:
    return _get_url(base(), 'v1/monitor/alerts')


def alert_rule(alert_rule: str) -> str:
    return _get_url(base(), 'v1/monitor/alertrules/{}'.format(alert_rule))


def applications() -> str:
    return _get_url(base(), 'v1/applications')


def attacks() -> str:
    return _get_url(base(), 'v1/attacks')


def events(execution_id: str) -> str:
    return _get_url(base(), 'v1/executions/{}/events'.format(execution_id))


def executions() -> str:
    return _get_url(base(), 'v1/executions')


def experiment() -> str:
    return _get_url(base(), 'v1/experiments')


def scripts() -> str:
    return _get_url(base(), 'v1/scripts')


def _get_url(base: str, address: str):
    base = base if base.endswith("/") else base + "/"
    return parse.urljoin(base, address)
