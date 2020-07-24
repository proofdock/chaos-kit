from requests import Session

from pdchaoskit.api import endpoints, get_error_message


def get_alert_rule(alert_rule: str, session: Session):
    response = session.get(endpoints.alert_rule(alert_rule), timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))


def get_alerts(alert_rule: str, status: str, start_date: str, end_date: str, session: Session):
    response = session.get(
        "{}?alert_rule={}&status={}&start_date={}&end_date={}"
        .format(endpoints.alerts(), alert_rule, status, start_date, end_date), timeout=30)
    if response.ok:
        return response.json()
    else:
        raise Exception(get_error_message(response))
