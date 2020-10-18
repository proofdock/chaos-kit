from unittest.mock import ANY, patch
import pytest
from chaoslib.exceptions import ActivityFailed

from pdchaoskit.application import actions

from tests.fixtures import data


@patch('pdchaoskit.alert.probes.client_session', spec=True)
@patch('pdchaoskit.application.actions.app_api', spec=True)
@patch('pdchaoskit.application.actions.get_loaded_settings', spec=True)
def test_action_start_attack(get_loaded_settings, app_api, session):
    # arrange
    get_loaded_settings.return_value = data.provide_settings()
    app_api.get_applications.return_value = [{'id': '1234'}]

    # act
    result = actions.start_attack('application_1', 'delay', '10')

    assert len(result) == 1
    assert result[0].get('id') == '1234'
    app_api.start_attack.assert_called_once_with('1234', 'delay', '10', ANY)


@patch('pdchaoskit.alert.probes.client_session', spec=True)
@patch('pdchaoskit.application.actions.app_api', spec=True)
@patch('pdchaoskit.application.actions.get_loaded_settings', spec=True)
def test_action_start_attack_no_application(get_loaded_settings, app_api, session):
    # arrange
    get_loaded_settings.return_value = data.provide_settings()
    app_api.get_applications.return_value = []

    # act
    with pytest.raises(ActivityFailed) as e:
        actions.start_attack('application_1', 'delay', '10')
    assert str(e.value) == 'Application application_1 not found.'


@patch('pdchaoskit.alert.probes.client_session', spec=True)
@patch('pdchaoskit.application.actions.app_api', spec=True)
@patch('pdchaoskit.application.actions.get_loaded_settings', spec=True)
def test_action_cancel_attack(get_loaded_settings, app_api, session):
    # arrange
    get_loaded_settings.return_value = data.provide_settings()
    app_api.get_applications.return_value = [{'id': '1234'}]

    # act
    result = actions.cancel_attack('application_1')

    assert len(result) == 1
    assert result[0].get('id') == '1234'
    app_api.cancel_attack.assert_called_once_with(['1234'], ANY)


@patch('pdchaoskit.alert.probes.client_session', spec=True)
@patch('pdchaoskit.application.actions.app_api', spec=True)
@patch('pdchaoskit.application.actions.get_loaded_settings', spec=True)
def test_action_cancel_all_attack(get_loaded_settings, app_api, session):
    # arrange
    get_loaded_settings.return_value = data.provide_settings()

    # act
    actions.cancel_attack()

    app_api.get_applications.assert_not_called()
    app_api.cancel_attack.assert_called_once_with([], ANY)
