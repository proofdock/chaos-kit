from typing import List

from chaoslib.discovery.discover import (discover_probes, discover_actions,
                                         initialize_discovery_result)
from chaoslib.types import DiscoveredActivities, Discovery
from logzero import logger

__version__ = '1.0.5'


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Proofdock capabilities from this extension.
    """
    logger.info("Discovering capabilities from pdchaoskit")

    discovery = initialize_discovery_result(
        "proofdock-chaos-kit", __version__, "pdchaoskit")
    discovery["activities"].extend(load_exported_activities())

    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_probes("pdchaoskit.alert.probes"))

    activities.extend(discover_actions("pdchaoskit.app.actions"))

    return activities
