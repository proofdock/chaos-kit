__version__ = '0.0.2'

from pdchaoskit.vcs import (GitInformationStrategy, PerforceInformationStrategy,
                            VcsInformationStrategy)


def vcs_information_factory() -> VcsInformationStrategy:
    if GitInformationStrategy().is_available():
        return GitInformationStrategy()

    if PerforceInformationStrategy().is_available():
        return PerforceInformationStrategy()

    raise NotImplementedError()
