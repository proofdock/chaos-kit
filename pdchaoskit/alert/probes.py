from datetime import datetime

from chaoslib.settings import get_loaded_settings
from chaoslib.types import Configuration, Secrets
from logzero import logger

from pdchaoskit.api.alerts import get_alert_rule, get_alerts
from pdchaoskit.api.session import client_session

__all__ = ["was_alert_fired"]


def was_alert_fired(
        alert_rule: str,
        configuration: Configuration = None,
        secrets: Secrets = None) -> bool:
    """
    Check if an alert was fired during an experiment run.

    Parameters
    ----------
    alert_rule : str, required
        Name of the alert rule for which check will be performed.
    """
    settings = get_loaded_settings()
    with client_session(verify_tls=False, settings=settings) as session:
        rule = get_alert_rule(alert_rule, session)

    # check latest state
    if 'latest_alert' in rule:
        latest_alert = rule.get('latest_alert')
        # latest alert is in fired state
        if latest_alert.get('status') == 'fired':
            logger.error('Alert %s is fired.', alert_rule)
            return True

    # check experiment period
    start_date = settings.get('run_context').get('execution').get('creation_time')
    end_date = datetime.utcnow().isoformat()
    with client_session(verify_tls=False, settings=settings) as session:
        alerts = get_alerts(alert_rule, 'fired', start_date, end_date, session)
    if len(alerts) > 0:
        for alert in alerts:
            logger.error('Alert %s fired at: %s', alert_rule,  alert.get('alert_time'))
        return True
    return False
