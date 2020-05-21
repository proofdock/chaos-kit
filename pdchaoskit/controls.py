import sys
from typing import Any, Dict, List

from chaoslib.exceptions import InterruptExecution
from chaoslib.settings import get_loaded_settings
from chaoslib.types import (Activity, Configuration, Experiment, Hypothesis,
                            Journal, Run, Secrets, Settings)
from logzero import logger

from pdchaoskit.settings import add_to_run_context

from .api.events import publish_event
from .api.executions import push_execution
from .api.session import client_session


def send_experiment_event(event: str, context: dict, state: dict,
                          settings: Settings):
    try:
        with client_session(verify_tls=False, settings=settings) as session:
            publish_event(event, context, state, settings, session)
    except Exception as ex:
        logger.error("Could not update experiment state in the Proofdock "
                     "cloud. %s", str(ex))
        logger.debug(ex)
        raise InterruptExecution()


def configure_control(configuration: Configuration = None,
                      secrets: Secrets = None, settings: Settings = None,
                      experiment: Experiment = None, **kwargs):
    """
    Configure the control's global state

    This is called once only per Chaos Toolkit's run and should be used to
    initialize any state your control may require.

    The `settings` are only passed when the control is declared in the
    settings file of the Chaos Toolkit.
    """

    pass


def cleanup_control():
    """
    Cleanup the control's global state

    Called once only during the experiment's execution.
    """

    settings = get_loaded_settings()

    if settings['run_context']['no_upload']:
        return

    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_value:
        state = {
            'error': str(exc_value)
        }

        send_experiment_event(
            event='abort-experiment', context=None,
            settings=settings, state=state)


def before_loading_experiment_control(context: str, state: Experiment,
                                      settings: Settings = None, **kwargs):
    pass


def after_loading_experiment_control(context: str, experiment: Experiment,
                                     settings: Settings = None, **kwargs):

    pass


def before_experiment_control(experiment: Experiment,
                              configuration: Configuration = None,
                              secrets: Secrets = None,
                              settings: Settings = None, **kwargs):
    """
    before-control of the experiment's execution

    Called by the Chaos Toolkit before the experiment's begin but after the
    configuration and secrets have been loaded.
    """

    if settings['run_context']['no_upload']:
        return

    try:
        logger.info('Creating experiment run in Proofdock...')
        with client_session(verify_tls=False, settings=settings) as session:
            execution = push_execution(settings, session)
        add_to_run_context(settings, 'execution_id', execution.get('id'))
        logger.info("New experiment run with id: '{}' created.".format(
            execution.get('id')))
    except Exception as ex:
        logger.error('Could not create experiment run in Proofdock cloud. %s',
                     str(ex))
        logger.debug(ex)
        raise InterruptExecution()

    send_experiment_event(
        event='before-experiment', context=None, state=None,
        settings=settings)


def after_experiment_control(context: Experiment, state: Journal,
                             configuration: Configuration = None,
                             secrets: Secrets = None,
                             settings: Settings = None, **kwargs):
    """
    after-control of the experiment's execution

    Called by the Chaos Toolkit after the experiment's completed. It passes the
    journal of the execution. At that stage, the after control has no influence
    over the execution however. Please see
    https://docs.chaostoolkit.org/reference/api/journal/#journal-elements
    for more information about the journal.
    """

    if settings['run_context']['no_upload']:
        return
    send_experiment_event(
        event='after-experiment', context=None, state=state,
        settings=settings)


def before_hypothesis_control(context: Hypothesis,
                              configuration: Configuration = None,
                              settings: Settings = None,
                              secrets: Secrets = None, **kwargs):
    """
    before-control of the hypothesis's execution

    Called by the Chaos Toolkit before the steady-state hypothesis is
    applied.
    """
    pass


def after_hypothesis_control(context: Hypothesis, state: Dict[str, Any],
                             configuration: Configuration = None,
                             settings: Settings = None,
                             secrets: Secrets = None, **kwargs):
    """
    after-control of the hypothesis's execution

    Called by the Chaos Toolkit after the steady-state hypothesis is
    complete. The `state` contains the result of the hypothesis. Refer to
    https://docs.chaostoolkit.org/reference/api/journal/#steady-state-outcomes
    for the description of that state.
    """
    if settings['run_context']['no_upload']:
        return
    send_experiment_event(
        event='after-hypothesis', context=context, state=state,
        settings=settings)


def before_method_control(context: Experiment,
                          configuration: Configuration = None,
                          settings: Settings = None,
                          secrets: Secrets = None, **kwargs):
    """
    before-control of the method's execution

    Called by the Chaos Toolkit before the activities of the method are
    applied.
    """
    pass


def after_method_control(context: Experiment, state: List[Run],
                         configuration: Configuration = None,
                         settings: Settings = None,
                         secrets: Secrets = None, **kwargs):
    """
    after-control of the method's execution

    Called by the Chaos Toolkit after the activities of the method have been
    applied. The `state` is the list of activity results. See
    https://docs.chaostoolkit.org/reference/api/journal/#run for more
    information.
    """
    if settings['run_context']['no_upload']:
        return
    send_experiment_event(
        event='after-method', context=context, state=state,
        settings=settings)


def before_rollback_control(context: Experiment,
                            configuration: Configuration = None,
                            settings: Settings = None,
                            secrets: Secrets = None, **kwargs):
    """
    before-control of the rollback's execution

    Called by the Chaos Toolkit before the actions of the rollback are
    applied.
    """
    pass


def after_rollback_control(context: Experiment, state: List[Run],
                           configuration: Configuration = None,
                           settings: Settings = None,
                           secrets: Secrets = None, **kwargs):
    """
    after-control of the rollback's execution

    Called by the Chaos Toolkit after the actions of the rollback have been
    applied. The `state` is the list of actions results. See
    https://docs.chaostoolkit.org/reference/api/journal/#run for more
    information.
    """
    if settings['run_context']['no_upload']:
        return
    send_experiment_event(
        event='after-rollback', context=context, state=state,
        settings=settings)


def before_activity_control(context: Activity,
                            configuration: Configuration = None,
                            settings: Settings = None,
                            secrets: Secrets = None, **kwargs):
    """
    before-control of the activity's execution

    Called by the Chaos Toolkit before the activity is applied.
    """
    pass


def after_activity_control(context: Activity, state: Run,
                           configuration: Configuration = None,
                           settings: Settings = None,
                           secrets: Secrets = None, **kwargs):
    """
    after-control of the activity's execution

    Called by the Chaos Toolkit before the activity is applied. The result of
    the execution is passed as `state`. See
    https://docs.chaostoolkit.org/reference/api/journal/#run for more
    information.
    """
    if settings['run_context']['no_upload']:
        return
    send_experiment_event(
        event='after-activity', context=context, state=state,
        settings=settings)
