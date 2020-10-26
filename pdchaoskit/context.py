import os

import click
from chaoslib.exceptions import InvalidSource
from logzero import logger

from pdchaoskit.vcs import vcs_information_factory

from .settings import (add_to_run_context, ensure_settings_are_valid,
                       update_settings_from_env)


def set_run_context(settings):

    try:
        update_settings_from_env(settings)
        ensure_settings_are_valid(settings)
    except Exception as x:
        logger.debug(x)
        logger.error("Your experiment results will not be uploaded to the cloud. " + str(x))
        raise Exception(str(x))

    params = click.get_current_context().params

    # configure upload options
    try:
        vcs_info = vcs_information_factory().as_dict(params.get('source'))
        settings = add_to_run_context(settings, 'vcs', vcs_info)
        add_to_run_context(settings, 'no_upload', False)
    except Exception as ex:
        logger.debug(ex)
        logger.warning(
            "Your experiment results will not be uploaded to the cloud. "
            "Run an experiment within your repository.")
        add_to_run_context(settings, 'no_upload', True)

    add_to_run_context(settings, 'description', params.get('description'))

    # set experiment path and verify if it is on local drive
    source = params.get('source')
    filename = click.format_filename(source)
    if not os.path.exists(filename):
        raise InvalidSource('Path "{}" does not exist.'.format(filename))
    add_to_run_context(settings, 'path', source)

    trigger = 'manual'
    if 'CHAOS_TASK_ID' in os.environ:
        trigger = 'ci'
    task = None
    if trigger == 'ci':
        task = {
            'id': os.environ.get('CHAOS_TASK_ID', None),
            'uri': os.environ.get('CHAOS_TASK_URI', None)
        }

    add_to_run_context(settings, 'trigger', trigger)
    add_to_run_context(settings, 'task', task)
