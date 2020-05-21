import os

import click
from chaoslib.exceptions import InvalidSource
from logzero import logger

from pdchaoskit import vcs_information_factory
from .settings import add_to_run_context


def set_run_context(context, settings):

    params = context.params

    # configure upload options
    no_upload = params.get('no_upload')
    add_to_run_context(settings, 'no_upload', no_upload)
    if not no_upload:
        try:
            vcs_info = vcs_information_factory().as_dict(params.get('source'))
            settings = add_to_run_context(settings, 'vcs', vcs_info)
        except Exception as ex:
            logger.debug(ex)
            raise Exception(
                "The command 'run' is disabled. Run an experiment "
                "within your repository or use '--no-upload' switch.")
    else:
        logger.warning(
            "Your experiment results will not be uploaded to the cloud.")

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
