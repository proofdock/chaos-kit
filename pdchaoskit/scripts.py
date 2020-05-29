from chaoslib.exceptions import FailedActivity
from chaoslib.settings import get_loaded_settings
from logzero import logger

from pdchaoskit.api.scripts import get_script_content
from pdchaoskit.api.session import client_session


def get_content(id: str) -> str:
    """Get a script's content"""
    settings = get_loaded_settings()

    try:
        with client_session(verify_tls=False, settings=settings) as session:
            return get_script_content(session, id)

    except Exception as ex:
        msg = "Unable to fetch script content. Reason: {}".format(str(ex))
        logger.error(msg)
        logger.debug(ex)
        raise FailedActivity(msg)
