from pathlib import Path
from typing import Any, cast
from unittest.mock import Mock, PropertyMock, patch

import pytest
from poetry.core.packages.dependency import Dependency
from poetry.core.packages.dependency_group import DependencyGroup
from poetry.core.packages.directory_dependency import DirectoryDependency
from poetry.poetry import Poetry
from poetry.utils.env import Env  # type: ignore  # Add this import

from tests.types import EventGenerator, MockEvent, SupportedCommand


@pytest.fixture
def mock_event_gen() -> EventGenerator[SupportedCommand]:
    def _factory(command_cls: type[SupportedCommand], disable_cache: bool = False) -> MockEvent:
        main_grp = DependencyGroup("main")
        main_grp.add_dependency(DirectoryDependency("packageB", Path("../packageB"), develop=True))
        main_grp.add_dependency(Dependency("numpy", "==1.5.0"))

        # Create a mock Poetry instance with all required attributes
        mock_poetry = Mock(spec=Poetry)
        mock_pyproject = Mock()
        mock_pyproject.poetry_config = {"name": "test-package", "version": "1.0.0"}
        mock_pyproject.file = Mock()

        # Fix: Set up proper Poetry attribute hierarchy
        mock_poetry._pyproject = mock_pyproject  # Set the private attribute directly
        type(mock_poetry).pyproject = PropertyMock(return_value=mock_pyproject)

        # Fix: Use actual Path objects instead of Mock
        package_path = Path("/monorepo_root/packageA")
        mock_poetry.pyproject_path = package_path / "pyproject.toml"
        mock_poetry.file = Mock()
        mock_poetry.file.parent = package_path
        mock_poetry.file.read = Mock(return_value={"tool": {"poetry": {"version": "1.0.0"}}})

        mock_poetry.package = Mock()
        mock_poetry.package.name = "packageA"
        mock_poetry.package.dependency_group = Mock(return_value=main_grp)
        mock_poetry.locker = Mock()
        mock_poetry.pool = Mock()
        mock_poetry.config = Mock()
        mock_poetry.config.repository_cache_directory = Path("/tmp/poetry/cache")
        mock_poetry.config.installer_max_workers = 4
        mock_poetry.disable_cache = disable_cache

        # Create command mock with all required attributes
        mock_command = Mock(spec=command_cls)
        mock_command.poetry = mock_poetry
        mock_command.option = Mock(return_value=False)
        mock_command.io = Mock()

        # Fix: Properly mock the environment
        mock_env = Mock(spec=Env)
        mock_env.sys_path = [
            str(Path("/monorepo_root/.venv/lib/python3.8/site-packages")),
            str(Path("/usr/lib/python3.8/site-packages")),
        ]
        mock_env.get_site_packages = Mock(
            return_value=Path("/monorepo_root/.venv/lib/python3.8/site-packages")
        )
        mock_env.get_paths = Mock(
            return_value={"purelib": "/monorepo_root/.venv/lib/python3.8/site-packages"}
        )
        mock_env.exists = Mock(return_value=True)
        mock_env.is_venv = Mock(return_value=True)
        mock_command.env = mock_env

        # Fix: Mock installer for command
        with patch("poetry.installation.installer.Installer") as mock_installer_cls:
            mock_installer = Mock()
            mock_installer_cls.return_value = mock_installer
            mock_command.set_poetry = Mock()
            mock_command.set_installer = Mock()
            mock_command.set_env = Mock()

            # Create event mock with all required attributes
            mock_event = Mock()
            mock_event.command = mock_command
            mock_event.io = mock_command.io
            mock_event.is_debug = Mock(return_value=False)
            mock_event.is_quiet = Mock(return_value=False)
            mock_event.is_verbose = Mock(return_value=False)
            mock_event.has_terminated = Mock(return_value=False)
            mock_event.output = ""
            mock_event.error_output = ""
            mock_event.set_exit_code = Mock()

            return cast(MockEvent, mock_event)

    return _factory


@pytest.fixture
def mock_terminate_event_gen(mock_event_gen: EventGenerator[SupportedCommand]):
    def _factory(command_cls: type[SupportedCommand], disable_cache: bool = False) -> Any:
        from cleo.events.console_terminate_event import ConsoleTerminateEvent

        mock_event = mock_event_gen(command_cls, disable_cache)
        mock_io = mock_event.io
        mock_command = mock_event.command
        del mock_event

        mock_terminate_event = Mock(spec=ConsoleTerminateEvent)
        mock_terminate_event.command = mock_command
        mock_terminate_event.io = mock_io

        return mock_terminate_event

    return _factory
