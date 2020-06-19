import json
from datetime import datetime
from unittest.mock import Mock, patch

from pdchaoskit.api.events import publish_event
from requests import Session

from tests.fixtures import data


@patch('pdchaoskit.api.events.datetime', spec=True)
def test_api_publish_event(datetime_mock):
    # arrange
    context = {'context': 'context_value'}
    state = {'state': 'state_value'}
    datetime_mock.utcnow.return_value = datetime(2020, 6, 19, 9, 12, 49, 663318)
    settings = data.provide_settings()
    session = Mock(Session)

    # act
    publish_event('test_event', context, state, settings, session)

    # assert
    expected_data = json.dumps({
        'name': "test_event",
        'state': state,
        'context': context,
        'timestamp': datetime(2020, 6, 19, 9, 12, 49, 663318).isoformat()
    })
    session.post.assert_called_once_with(
        '/v1/executions/1234/events',
        data=expected_data,
        timeout=30)
