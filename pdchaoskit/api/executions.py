import json
from typing import Dict

from requests import Session

from pdchaoskit.api import endpoints, get_error_message


def push_execution(settings: Dict, session: Session):
    body = request_body_as_jsonstring(settings)
    path = settings.get('run_context')['path']

    with open(path, 'rb') as file:
        return push(session, body, file)


def request_body_as_jsonstring(settings):
    # prepare payload as dict
    ctx = settings.get('run_context')
    payload = {
        'vcs': ctx['vcs'],
        'description': ctx['description'],
        'trigger': ctx['trigger'],
        'task': ctx['task']
    }
    # payload as json string
    body = {
        'body': json.dumps(payload)
    }
    return body


def push(session, body, file):
    files = {
        'file': file
    }

    response = session.post(endpoints.executions(),
                            data=body,
                            files=files,
                            timeout=30)

    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))
