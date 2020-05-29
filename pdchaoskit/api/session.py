from contextlib import contextmanager
from typing import Generator

from chaoslib.types import Settings
from requests import Session

from pdchaoskit.settings import get_api_token, get_api_url


@contextmanager
def client_session(verify_tls: bool = True, settings: Settings = None) -> Generator[Session, None, None]:

    # prepare auth token
    api_url = get_api_url(settings)
    api_token = get_api_token(settings, api_url)
    headers = {
        "Authorization": "Bearer {}".format(api_token),
    }

    with Session() as s:
        s.base_url = api_url
        s.headers.update(headers)
        s.verify = verify_tls
        yield s
