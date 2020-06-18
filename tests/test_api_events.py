from unittest.mock import Mock

from pdchaoskit.api.events import publish_event
from requests import Session

from tests.fixtures import data


def test_api_publish_event():
    # arrange   
    context = {'context': 'context_value'}
    state = {'state': 'state_value'}
    settings = data.provide_settings()
    session = Mock(Session)

    # act
    publish_event('test_event', context, state, settings, session)

    # assert
    session.post.assert_called_once_with(
        '/v1/executions/1234/events',
        data="""{"name": "test_event", "state": {"state": "state_value"}, "context": {"context": "context_value"}}""",
        timeout=30)
