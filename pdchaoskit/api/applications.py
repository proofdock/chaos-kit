from requests import Session
import json
from pdchaoskit.api import endpoints, get_error_message
from typing import List


def get_applications(app_name: str, session: Session):
    response = session.get(
        "{}?name={}"
        .format(endpoints.applications(), app_name), timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))


def start_attack(app_id: str, name: str, value: str, session: Session):
    data = json.dumps({
        'application_id': app_id,
        'name': '',
        'actions': [
            {
                'name': name,
                'value': str(value),
            }
        ]
    })

    response = session.post(endpoints.attacks(), data=data, timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))


def cancel_attack(app_ids: List[str], session: Session):
    data = json.dumps({
        'application_ids': app_ids if app_ids else []
    })
    response = session.post("{}/cancel".format(endpoints.attacks()), data=data, timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))
