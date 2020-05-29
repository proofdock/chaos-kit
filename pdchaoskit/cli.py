# -*- coding: utf-8 -*-
import io
import json
from typing import Dict, Any
from urllib.parse import urlparse

import click
from chaoslib.control import load_global_controls
from chaoslib.exceptions import ChaosException, InvalidSource
from chaoslib.experiment import ensure_experiment_is_valid, run_experiment
from chaoslib.loader import load_experiment
from chaoslib.notification import RunFlowEvent, notify
from chaoslib.settings import get_loaded_settings, load_settings, save_settings
from chaoslib.types import Journal
from chaostoolkit import encoder
from chaostoolkit.cli import cli
from logzero import logger
from tabulate import tabulate

from .api.experiments import get_experiments
from .api.session import client_session
from .context import set_run_context
from .settings import (ensure_settings_are_valid, set_settings, get_api_url, update_settings_from_env,
                       DEFAULT_PROOFDOCK_API_URL)


@cli.command()
@click.option('--description', default=None,
              help='Additional description of the experiment run.')
@click.option('--journal-path', default="./journal.json",
              help='Path where to save the journal from the execution.')
@click.option('--dry', is_flag=True,
              help='Run the experiment without executing activities.')
@click.option('--no-upload', is_flag=True,
              help='Do not upload the experiment and results after running.')
@click.option('--no-validation', is_flag=True,
              help='Do not validate the experiment before running.')
@click.argument('source')
@click.pass_context
def run(ctx: click.Context,
        source: str,
        description: str,
        journal_path: str = "./journal.json",
        dry: bool = False,
        no_upload: bool = False,
        no_validation: bool = False,
        no_exit: bool = False,
        ) -> Journal:
    """Run the experiment loaded from SOURCE - must be a local file."""

    settings = __load_settings(ctx)

    try:
        set_run_context(ctx, settings)
    except Exception as x:
        logger.error(str(x))
        logger.debug(x)
        ctx.exit(1)

    load_global_controls(settings)

    try:
        filename = click.format_filename(source)
        experiment = load_experiment(filename, settings)
    except InvalidSource as x:
        logger.error(str(x))
        logger.debug(x)
        ctx.exit(1)

    notify(settings, RunFlowEvent.RunStarted, experiment)

    if not no_validation:
        try:
            ensure_experiment_is_valid(experiment)
        except ChaosException as x:
            logger.error(str(x))
            logger.debug(x)
            ctx.exit(1)

    experiment["dry"] = dry

    journal = run_experiment(experiment, settings=settings)
    has_deviated = journal.get("deviated", False)
    has_failed = journal["status"] != "completed"

    with io.open(journal_path, "w") as r:
        json.dump(journal, r, indent=2, ensure_ascii=False, default=encoder)

    if journal["status"] == "completed":
        notify(settings, RunFlowEvent.RunCompleted, journal)
    elif has_failed:
        notify(settings, RunFlowEvent.RunFailed, journal)

        if has_deviated:
            notify(settings, RunFlowEvent.RunDeviated, journal)

    if (has_failed or has_deviated) and not no_exit:
        ctx.exit(1)

    return journal


@cli.command(help="Configure Proofdock chaos-kit")
@click.option('--token',
              help="Token value",
              required=False, type=str)
@click.option('--default-api-url',
              help="Default API",
              required=False, type=str)
@click.pass_context
def configure(ctx: click.Context,
              token: str = None,
              default_api_url: str = None):
    settings_path = ctx.obj["settings_path"]
    settings = load_settings(settings_path) or {}

    # set default url for API calls
    api_url = get_api_url(settings)
    if default_api_url:
        api_url = urlparse(default_api_url)
        api_url = \
            "{}://{}{}".format(
                api_url.scheme,
                api_url.netloc,
                api_url.path)
    api_url = api_url or DEFAULT_PROOFDOCK_API_URL

    set_settings(settings, api_url, token)
    save_settings(settings, settings_path)
    click.echo(click.style(
        "Configuration saved at {}".format(settings_path), fg='green'))


@cli.group(help="Experiment management options")
@click.pass_obj
def experiment(config):
    pass


@experiment.command(help="List all experiments in your project")
@click.pass_context
def list(ctx: click.Context):
    settings = __load_settings(ctx)

    try:
        with client_session(verify_tls=False, settings=settings) as session:
            experiments = get_experiments(session)

        table = {'Id': [], 'Title': [], 'Latest execution': []}
        for exp in experiments:
            table['Id'].append(exp.get('id'))
            table['Title'].append(exp.get('title'))
            table['Latest execution'].append(
                (exp.get('latest_execution')
                 if exp.get('latest_execution') else {}).get(
                    'start_time', 'never'))
        click.echo(tabulate(table, headers="keys", showindex="always"))

    except Exception as ex:
        logger.error("Unable to list experiments. %s", str(ex))
        logger.debug(ex)
        ctx.exit(1)


###################################################
# PRIVATE HELPERS
###################################################
def __load_settings(ctx: click.Context) -> Dict[str, Any]:
    settings_path = ctx.obj["settings_path"]
    settings = load_settings(settings_path) or get_loaded_settings()

    try:
        settings = update_settings_from_env(settings)
        ensure_settings_are_valid(settings)
        return settings
    except Exception as x:
        logger.error(str(x))
        logger.debug(x)
        ctx.exit(1)
