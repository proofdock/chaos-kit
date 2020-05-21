import os
import subprocess
import urllib
from abc import ABCMeta, abstractmethod
from pathlib import Path, PurePosixPath
from typing import Dict

from logzero import logger


class VcsInformationStrategy(metaclass=ABCMeta):
    """
    Declare an interface common to all supported version control systems.
    """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Whether the strategy is applicable
        :return: true if applicable, else false
        """
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> str:
        """
        Return the vcs type.
        :return: the vcs type
        """
        raise NotImplementedError

    @abstractmethod
    def get_top_level_directory(self) -> str:
        """
        Show the absolute path of the top-level directory of the working tree
        :return: the absolute path of the top-level directory
        """
        raise NotImplementedError

    def get_relative_path(self, source: str) -> str:
        """
        Show the path of the given source file relative to the top-level
        directory
        :param source: the give file
        :return: the relative path of the give source file
        """
        abs_top_level_dir = os.path.normcase(
            os.path.normpath(self.get_top_level_directory()))
        abs_working_dir = os.path.normcase(
            os.path.normpath(os.path.join(os.getcwd(), source)))

        if not abs_working_dir.startswith(abs_top_level_dir):
            logger.debug(
                "Repository top level directory is '{}'. Specified working directory is '{}'".format(
                    abs_top_level_dir, {abs_working_dir}))
            raise Exception(
                "Experiment file is not inside current "
                + self.get_type() + " directory.")

        result = abs_working_dir.replace(abs_top_level_dir, "")
        return self.norm_to_posix_path(result)

    @staticmethod
    def norm_to_posix_path(path):
        # remove leading path separator in Windows
        path = path.strip(os.sep)
        # remove leading path separator in Linux
        path = path.strip(os.altsep)
        return str(PurePosixPath(Path(path)))

    @abstractmethod
    def get_repository_uri(self) -> str:
        """
        The full repository URI
        :return: the repository URI
        """
        raise NotImplementedError

    @abstractmethod
    def get_revision(self) -> str:
        """
        The full SHA-1 object name (40-byte hexadecimal string)
        :return: returns the commit object with its SHA-1
        """
        raise NotImplementedError

    @abstractmethod
    def get_repository_id(self) -> str:
        """
        The repository id that uniquely identifies it
        :return: the repository id
        """
        raise NotImplementedError

    def as_dict(self, source: str) -> Dict[str, str]:
        return {
            'id': self.get_repository_id(),
            'type': self.get_type(),
            'path': self.get_relative_path(source),
            'repository_uri': self.get_repository_uri(),
            'revision': self.get_revision(),
        }


class GitInformationStrategy(VcsInformationStrategy):
    """
    Implement the algorithm using the Git interface.
    """

    def get_type(self) -> str:
        return "git"

    def is_available(self) -> bool:
        result = subprocess.Popen(
            ['git', 'status'], stdout=subprocess.PIPE).wait()
        return result == 0

    def get_top_level_directory(self) -> str:
        result = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel']).decode('utf-8').strip()
        return result

    def get_repository_uri(self) -> str:
        url = subprocess.check_output(
            ['git', 'config', '--get', 'remote.origin.url']
        ).decode('utf-8').strip()
        return self.norm_uri(url)

    @staticmethod
    def norm_uri(uri: str) -> str:
        if uri.startswith('https') or uri.startswith('http'):
            parsed = list(urllib.parse.urlsplit(uri))
            parsed[1] = parsed[1].split('@')[-1]  # erase username + password
            parsed[3] = ''  # erase query
            parsed[4] = ''  # erase fragments
            result = urllib.parse.urlunsplit(parsed)
            return result

        else:
            return uri

    def get_revision(self) -> str:
        result = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        return result

    def get_repository_id(self) -> str:
        rev_list = subprocess.Popen(
            ('git', 'rev-list', '--parents', 'HEAD'),
            stdout=subprocess.PIPE)
        result = subprocess.check_output(
            ['tail', '-1'], stdin=rev_list.stdout
        ).decode('utf-8').strip()
        rev_list.wait()
        return result


class PerforceInformationStrategy(VcsInformationStrategy):
    """
    Implement the algorithm using the Perforce interface.
    """

    def get_type(self) -> str:
        return "perforce"

    def is_available(self) -> bool:
        raise NotImplementedError

    def get_top_level_directory(self) -> str:
        raise NotImplementedError

    def get_repository_uri(self) -> str:
        raise NotImplementedError

    def get_revision(self) -> str:
        raise NotImplementedError

    def get_repository_id(self) -> str:
        raise NotImplementedError
