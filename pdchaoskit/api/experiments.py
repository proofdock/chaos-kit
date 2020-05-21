from requests import Session

from pdchaoskit.api import endpoints, get_error_message


def get_experiments(session: Session):
    response = session.get(endpoints.experiment(), timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))
