import os
import subprocess
from unittest import mock

import pytest

from pdchaoskit import GitInformationStrategy


class TestGitInformationStrategy:
    def test_get_type(self):
        git_vcs = GitInformationStrategy()
        assert git_vcs.get_type() == 'git'

    def test_get_type_is_not_git(self):
        git_vcs = GitInformationStrategy()
        assert git_vcs.get_type() != 'p4c'

    def test_is_available(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'Popen') as mocked_popen:
            mocked_popen.return_value.wait.return_value = 0
            assert git_vcs.is_available() is True

    def test_get_top_level_directory(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            # Usually sth like '/home/vsts/work/1/s'
            passed_arg = os.path.join('home', 'vsts', 'work', '1', 's')
            mocked_subprocess.return_value = passed_arg.encode('utf-8')
            assert git_vcs.get_top_level_directory() == os.path.normcase(passed_arg)

    def test_get_repository_uri(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            mocked_subprocess.return_value = 'https://dev.azure.com/proofdockio/chaos/_git/core'.encode(
                'utf-8')
            assert git_vcs.get_repository_uri(
            ) == 'https://dev.azure.com/proofdockio/chaos/_git/core'

    def test_get_repository_uri_with_credentials(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            mocked_subprocess.return_value = 'https://marcin:secret@dev.azure.com' \
                                             '/proofdockio/chaos/_git/core'.encode(
                                                 'utf-8')
            assert git_vcs.get_repository_uri(
            ) == 'https://dev.azure.com/proofdockio/chaos/_git/core'

    @mock.patch('pdchaoskit.vcs.subprocess', spec=True)
    def test_get_repository_id(self, mocked_subprocess):
        # arrange
        mocked_subprocess.check_output.return_value = \
            '154769f64d88338667a4910355dd56c80a4da994'.encode('utf-8')

        # act & assert
        git_vcs = GitInformationStrategy()
        assert git_vcs.get_repository_id() == \
            '154769f64d88338667a4910355dd56c80a4da994'

    def test_get_revision(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            mocked_subprocess.return_value = '52a2b0b3-5f21-11ea-9297-028037ec0200'.encode(
                'utf-8')
            assert git_vcs.get_revision() == '52a2b0b3-5f21-11ea-9297-028037ec0200'

    def test_get_relative_path_with_absolute_source(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            mocked_subprocess.return_value = '/Users/runner/runners/2.165.0/work/1/s'.encode(
                'utf-8')
            with mock.patch.object(os, 'getcwd') as mocked_os:
                mocked_os.return_value = '/Users/runner/runners/2.165.0/work/1/s'
                assert git_vcs.get_relative_path(
                    '/Users/runner/runners/2.165.0/work/1/s/path/to/experiment.yml') == 'path/to/experiment.yml'

    def test_get_relative_path_with_relative_source(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            mocked_subprocess.return_value = '/Users/runner/runners/2.165.0/work/1/s'.encode(
                'utf-8')
            with mock.patch.object(os, 'getcwd') as mocked_os:
                mocked_os.return_value = '/Users/runner/runners/2.165.0/work/1/s'
                assert git_vcs.get_relative_path(
                    'path/to/experiment.yml') == 'path/to/experiment.yml'

    def test_get_relative_path_with_relative_source_fail(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            mocked_subprocess.return_value = os.path.join(
                'a', '1', 's').encode('utf-8')
            with mock.patch.object(os, 'getcwd') as mocked_os:
                mocked_os.return_value = os.path.join('a', 'wrong', 's')
                passed_arg = os.path.join('path', 'to', 'experiment.yml')
                with pytest.raises(Exception):
                    git_vcs.get_relative_path(passed_arg)

    def test_get_relative_path_with_not_normalized_source_fail(self):
        git_vcs = GitInformationStrategy()
        with mock.patch.object(subprocess, 'check_output') as mocked_subprocess:
            mocked_subprocess.return_value = '/Users/work/1/s'.encode('utf-8')
            with mock.patch.object(os, 'getcwd') as mocked_os:
                mocked_os.return_value = '/Users/work/1/s'
                # should throw here
                passed_arg = '../path/to/experiment.yml'
                with pytest.raises(Exception):
                    git_vcs.get_relative_path(passed_arg)
