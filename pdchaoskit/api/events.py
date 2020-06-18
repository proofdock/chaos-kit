import json

from requests import Session

from pdchaoskit.api import endpoints, get_error_message


def publish_event(name, context, state, settings, session: Session):
    id = settings.get('run_context').get('execution_id', None)
    if not id:
        raise Exception("Experiment run identifier cannot be empty.")
    data = json.dumps({
        'name': name,
        'state': state,
        'context': context
    })
    response = session.post(endpoints.events(id), data=data, timeout=30)
    if not response.ok:
        raise Exception(get_error_message(response))
