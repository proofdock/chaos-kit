# -*- coding: utf-8 -*-
from typing import Any, Dict
from urllib.parse import urlparse

import click
from chaoslib.settings import get_loaded_settings, load_settings, save_settings
from chaostoolkit.cli import cli
from logzero import logger
from tabulate import tabulate

from .api.experiments import get_experiments
from .api.session import client_session
from .settings import (DEFAULT_PROOFDOCK_API_URL, ensure_settings_are_valid,
                       get_api_url, set_settings, update_settings_from_env)


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
