"""Tests for LockModifier."""

from pathlib import Path
from typing import cast
from unittest.mock import MagicMock, patch

from cleo.events.console_command_event import ConsoleCommandEvent
from poetry.console.commands.install import InstallCommand
from poetry.console.commands.lock import LockCommand
from poetry.console.commands.update import UpdateCommand
from poetry.factory import Factory

from poetflow.plugins.lock import LockModifier
from poetflow.types.config import MonorangerConfig
from tests.types import EventGenerator


def test_executes_modifications_for_lock_command(
    mock_event_gen: EventGenerator[LockCommand], mock_root_poetry: MagicMock
) -> None:
    """Test lock modifier with lock command."""
    mock_event = mock_event_gen(LockCommand, True)
    mock_command = cast(MagicMock, mock_event.command)
    mock_command.poetry = MagicMock()
    mock_command.poetry.file = MagicMock()
    mock_command.poetry.file.parent = Path("/fake/path")
    mock_command.poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    mock_command.poetry.disable_cache = False
    mock_command.poetry.config = MagicMock()
    mock_command.poetry.config.installer_max_workers = 4

    # Mock root poetry config
    mock_root_poetry.config = MagicMock()
    mock_root_poetry.config.installer_max_workers = 4

    # Create plugin instance
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    plugin = LockModifier(config)

    # Execute plugin with mocked Factory
    with patch.object(Factory, "create_poetry", return_value=mock_root_poetry):
        plugin.execute(cast(ConsoleCommandEvent, mock_event))

    # Verify poetry was set
    mock_command.set_poetry.assert_called_once_with(mock_root_poetry)


def test_executes_modifications_for_install_command(
    mock_event_gen: EventGenerator[InstallCommand], mock_root_poetry: MagicMock
) -> None:
    """Test lock modifier with install command."""
    mock_event = mock_event_gen(InstallCommand, True)
    mock_command = cast(MagicMock, mock_event.command)
    mock_command.poetry = MagicMock()
    mock_command.poetry.file = MagicMock()
    mock_command.poetry.file.parent = Path("/fake/path")
    mock_command.poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    mock_command.poetry.disable_cache = False
    mock_command.poetry.config = MagicMock()
    mock_command.poetry.config.installer_max_workers = 4

    # Mock root poetry config
    mock_root_poetry.config = MagicMock()
    mock_root_poetry.config.installer_max_workers = 4

    # Create plugin instance
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    plugin = LockModifier(config)

    # Execute plugin with mocked Factory
    with patch.object(Factory, "create_poetry", return_value=mock_root_poetry):
        plugin.execute(cast(ConsoleCommandEvent, mock_event))

    # Verify poetry was set
    mock_command.set_poetry.assert_called_once_with(mock_root_poetry)


def test_executes_modifications_for_update_command(
    mock_event_gen: EventGenerator[UpdateCommand], mock_root_poetry: MagicMock
) -> None:
    """Test lock modifier with update command."""
    mock_event = mock_event_gen(UpdateCommand, True)
    mock_command = cast(MagicMock, mock_event.command)
    mock_command.poetry = MagicMock()
    mock_command.poetry.file = MagicMock()
    mock_command.poetry.file.parent = Path("/fake/path")
    mock_command.poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    mock_command.poetry.disable_cache = False
    mock_command.poetry.config = MagicMock()
    mock_command.poetry.config.installer_max_workers = 4

    # Mock root poetry config
    mock_root_poetry.config = MagicMock()
    mock_root_poetry.config.installer_max_workers = 4

    # Create plugin instance
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    plugin = LockModifier(config)

    # Execute plugin with mocked Factory
    with patch.object(Factory, "create_poetry", return_value=mock_root_poetry):
        plugin.execute(cast(ConsoleCommandEvent, mock_event))

    # Verify poetry was set
    mock_command.set_poetry.assert_called_once_with(mock_root_poetry)
