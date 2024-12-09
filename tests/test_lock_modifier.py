"""Tests for the LockModifier class"""

from pathlib import Path
from typing import cast
from unittest.mock import Mock, patch

import pytest
from cleo.events.console_command_event import ConsoleCommandEvent
from poetry.console.commands.lock import LockCommand  # type: ignore
from poetry.factory import Factory  # type: ignore
from poetry.poetry import Poetry  # type: ignore
from poetry.utils.env import Env  # type: ignore

from poetflow.plugins.lock import LockModifier
from poetflow.types.config import MonorangerConfig
from tests.types import MockCommand, MockEvent


@pytest.fixture
def mock_poetry() -> Mock:
    poetry = Mock(spec=Poetry)
    poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    poetry.disable_cache = False
    poetry.locker = Mock()
    poetry.locker.lock_data = {"metadata": {"version": "1.0.0"}}
    poetry.config = Mock()
    poetry.config.installer_max_workers = 4
    poetry.config.repository_cache_directory = Path("/tmp/poetry/cache")
    poetry.package = Mock()  # Add package mock
    poetry.pool = Mock()  # Add pool mock
    return poetry


@pytest.fixture
def mock_command(mock_poetry: Mock) -> MockCommand:
    command = Mock(LockCommand)
    command.poetry = mock_poetry
    command.io = Mock()
    
    # Fix: Properly mock the environment
    mock_env = Mock(spec=Env)  # Add spec=Env
    mock_env.sys_path = [
        str(Path("/monorepo_root/.venv/lib/python3.8/site-packages")),
        str(Path("/usr/lib/python3.8/site-packages")),
    ]
    mock_env.get_site_packages = Mock(return_value=Path("/monorepo_root/.venv/lib/python3.8/site-packages"))
    mock_env.get_paths = Mock(return_value={"purelib": "/monorepo_root/.venv/lib/python3.8/site-packages"})
    mock_env.exists = Mock(return_value=True)
    mock_env.is_venv = Mock(return_value=True)
    command.env = mock_env
    
    command.set_poetry = Mock()
    command.set_installer = Mock()
    return cast(MockCommand, command)


@pytest.fixture
def mock_event(mock_command: MockCommand) -> MockEvent:
    event = Mock(spec=ConsoleCommandEvent)
    event.command = mock_command
    event.io = mock_command.io
    return cast(MockEvent, event)


def test_lock_modifier_initialization():
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    modifier = LockModifier(config)
    assert modifier.plugin_conf == config


@patch.object(Factory, "create_poetry")
def test_lock_modifier_execute(
    mock_create_poetry: Mock,
    mock_event: MockEvent,
    mock_poetry: Mock,
) -> None:
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    modifier = LockModifier(config)

    mock_root_poetry = Mock(spec=Poetry)
    mock_root_poetry.locker = Mock()
    mock_root_poetry.locker.lock_data = {"metadata": {"version": "1.0.0"}}
    mock_root_poetry.config = Mock()
    mock_root_poetry.config.installer_max_workers = 4
    mock_root_poetry.config.repository_cache_directory = Path("/tmp/poetry/cache")
    mock_root_poetry.package = Mock()
    mock_root_poetry.pool = Mock()
    mock_create_poetry.return_value = mock_root_poetry

    # Fix: Mock environment for root poetry
    mock_env = Mock(spec=Env)
    mock_env.sys_path = [
        str(Path("/monorepo_root/.venv/lib/python3.8/site-packages")),
        str(Path("/usr/lib/python3.8/site-packages")),
    ]
    mock_env.get_site_packages = Mock(return_value=Path("/monorepo_root/.venv/lib/python3.8/site-packages"))
    mock_env.get_paths = Mock(return_value={"purelib": "/monorepo_root/.venv/lib/python3.8/site-packages"})
    mock_env.exists = Mock(return_value=True)
    mock_env.is_venv = Mock(return_value=True)
    mock_event.command.env = mock_env

    # Create a mock installer
    mock_installer = Mock()
    
    # Patch the Installer class in the correct module
    with (
        patch("poetflow.plugins.lock.Installer", return_value=mock_installer),
        patch.object(mock_event.command, "set_installer") as mock_set_installer
    ):
        modifier.execute(mock_event)

        mock_create_poetry.assert_called_once()
        assert mock_event.command.set_poetry.call_args == ((mock_root_poetry,),)
        mock_set_installer.assert_called_once_with(mock_installer)
