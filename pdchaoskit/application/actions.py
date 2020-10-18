# -*- coding: utf-8 -*-
import pdchaoskit.api.applications as app_api
from chaoslib.exceptions import ActivityFailed
from chaoslib.settings import get_loaded_settings
from chaoslib.types import Configuration, Secrets
from logzero import logger
from pdchaoskit.api.session import client_session

__all__ = ["start_attack", "cancel_attack"]


def start_attack(target: str, name: str, value: str,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """Start the attack on the application.

    **Be aware**: It may take up to 30s to propagate new attack configuration to all your applications.

    Parameters
    ----------
    target : str, required
        Application you want to attack, name provided during configuration of the 'Chaos Middleware'
    name : str, required
        Name of the attack, available options are:
        delay - delays the response of the request
        fault - raises an exception. The value takes the fully qualified name of the exception
    value : str, required
        number of seconds of delay - for a 'delay' attack
        fully qualified name of the exception - for a 'fault' attack
    """
    logger.debug(
        "Starting {}: configuration='{}', name='{}', value='{}', target='{}'"
        .format(start_attack.__name__, configuration, name, value, target))

    settings = get_loaded_settings()
    with client_session(verify_tls=False, settings=settings) as session:
        applications = app_api.get_applications(target, session)

    if not applications or len(applications) < 1:
        raise ActivityFailed("Application {} not found.".format(target))

    for application in applications:
        application_id = application.get('id')
        logger.info("Starting attack for application: {}, id: {}".format(target, application_id))
        with client_session(verify_tls=False, settings=settings) as session:
            app_api.start_attack(application_id, name, value, session)

    return applications


def cancel_attack(target: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """Cancel running attacks.

    **Be aware**: If no 'target' is provided all attacks will be stopped.

    Parameters
    ----------
    target : str, optional
        Application name for which an attack is to be canceled, name provided during configuration of the
        'Chaos Middleware'.
    """
    logger.debug(
        "Starting {}: configuration='{}', target='{}'"
        .format(cancel_attack.__name__, configuration, target))

    settings = get_loaded_settings()
    applications = []
    if target:
        with client_session(verify_tls=False, settings=settings) as session:
            applications = app_api.get_applications(target, session)
        if not applications or len(applications) < 1:
            raise ActivityFailed("Application {} not found.".format(target))
        else:
            logger.info(
                "Cancel attacks on following applications: {}."
                .format([app.get('name') for app in applications]))
    else:
        logger.info("Cancel all attacks.")

    with client_session(verify_tls=False, settings=settings) as session:
        app_api.cancel_attack([app.get('id') for app in applications], session)

    return applications
