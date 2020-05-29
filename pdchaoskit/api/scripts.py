from requests import Session

from pdchaoskit.api import endpoints, get_error_message


def get_script_content(session: Session, id: str):
    """Fetch the script's content"""
    response = session.get(endpoints.scripts() + '/{}'.format(id), timeout=30)
    if response.ok:
        return response.text
    else:
        raise Exception(get_error_message(response))
