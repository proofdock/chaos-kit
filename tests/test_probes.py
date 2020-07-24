from unittest.mock import ANY, patch

from tests.fixtures import data

from pdchaoskit import probes


@patch('pdchaoskit.probes.client_session', spec=True)
@patch('pdchaoskit.probes.get_alert_rule', spec=True)
@patch('pdchaoskit.probes.get_alerts', spec=True)
@patch('pdchaoskit.probes.get_loaded_settings', spec=True)
def test_probe_was_alert_fired_no_alerts(get_loaded_settings, get_alerts, get_alert_rule, session):
    # arrange
    get_alert_rule.return_value = {"latest_alert": {"status": "resolved"}}
    get_alerts.return_value = []
    get_loaded_settings.return_value = data.provide_settings()

    # act
    result = probes.was_alert_fired('rule_1')

    assert result is False
    get_alert_rule.assert_called_once_with('rule_1', ANY)
    get_alerts.assert_called_once_with('rule_1', 'fired', ANY, ANY, ANY)


@patch('pdchaoskit.probes.client_session', spec=True)
@patch('pdchaoskit.probes.get_alert_rule', spec=True)
def test_probe_was_alert_fired_latest_fired(get_alert_rule, session):
    # arrange
    get_alert_rule.return_value = {"latest_alert": {"status": "fired"}}

    # act
    result = probes.was_alert_fired('rule_1')

    assert result is True
    get_alert_rule.assert_called_once_with('rule_1', ANY)


@patch('pdchaoskit.probes.client_session', spec=True)
@patch('pdchaoskit.probes.get_alert_rule', spec=True)
@patch('pdchaoskit.probes.get_alerts', spec=True)
@patch('pdchaoskit.probes.get_loaded_settings', spec=True)
def test_probe_was_alert_fired_fired_during_experiment(get_loaded_settings, get_alerts, get_alert_rule, session):
    # arrange
    get_alert_rule.return_value = {"latest_alert": {"status": "resolved"}}

    get_alerts.return_value = [{"alert_time": "2020-07-23T19:49:59Z"}]
    get_loaded_settings.return_value = data.provide_settings()

    # act
    result = probes.was_alert_fired('rule_1')

    assert result is True
    get_alert_rule.assert_called_once_with('rule_1', ANY)
