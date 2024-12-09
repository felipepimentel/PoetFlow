"""Tests for the LockModifier class"""

from pathlib import Path
from typing import cast
from unittest.mock import Mock, patch

import pytest
from poetry.console.commands.lock import LockCommand  # type: ignore
from poetry.factory import Factory  # type: ignore

from poetflow.config import MonorangerConfig
from poetflow.plugins.lock import LockModifier
from tests.types import ConsoleCommandEvent


@pytest.fixture
def mock_poetry() -> Mock:
    poetry = Mock()
    poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    poetry.disable_cache = False
    poetry.locker = Mock()
    poetry.locker.lock_data = {"metadata": {"version": "1.0.0"}}
    poetry.config = Mock()
    poetry.config.installer_max_workers = 4  # Add specific value for max_workers
    return poetry


@pytest.fixture
def mock_command(mock_poetry: Mock) -> Mock:
    command = Mock(spec=LockCommand)
    command.poetry = mock_poetry
    command.io = Mock()
    command.env = Mock()
    command.set_poetry = Mock()
    command.set_installer = Mock()
    return command


@pytest.fixture
def mock_event(mock_command: Mock) -> ConsoleCommandEvent:
    event = Mock(spec=ConsoleCommandEvent)
    event.command = mock_command
    event.io = mock_command.io
    return cast(ConsoleCommandEvent, event)


def test_lock_modifier_initialization():
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    modifier = LockModifier(config)
    assert modifier.plugin_conf == config


@patch.object(Factory, "create_poetry")
def test_lock_modifier_execute(
    mock_create_poetry: Mock,
    mock_event: ConsoleCommandEvent,
    mock_poetry: Mock
) -> None:
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    modifier = LockModifier(config)
    
    mock_root_poetry = Mock()
    mock_root_poetry.locker = Mock()
    mock_root_poetry.locker.lock_data = {"metadata": {"version": "1.0.0"}}
    mock_root_poetry.config = Mock()
    mock_root_poetry.config.installer_max_workers = 4  # Add specific value for max_workers
    mock_create_poetry.return_value = mock_root_poetry
    
    modifier.execute(mock_event)
    
    mock_create_poetry.assert_called_once()
    mock_event.command.set_poetry.assert_called_once_with(mock_root_poetry)
    mock_event.command.set_installer.assert_called_once()
