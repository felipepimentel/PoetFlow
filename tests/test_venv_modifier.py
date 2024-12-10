"""Tests for VenvModifier."""

from pathlib import Path
from typing import cast
from unittest.mock import MagicMock, patch

from cleo.events.console_command_event import ConsoleCommandEvent
from poetry.console.commands.env_command import EnvCommand
from poetry.console.commands.install import InstallCommand
from poetry.factory import Factory

from poetflow.plugins.venv import VenvModifier
from poetflow.types.config import MonorangerConfig
from tests.types import EventGenerator


def test_executes_modifications_for_env_command(
    mock_event_gen: EventGenerator[EnvCommand], mock_root_poetry: MagicMock
) -> None:
    """Test venv modifier with env command."""
    mock_event = mock_event_gen(EnvCommand, True)
    mock_command = cast(MagicMock, mock_event.command)

    # Mock poetry attributes
    mock_command.poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    mock_command.poetry.disable_cache = False

    # Mock Factory.create_poetry
    with patch.object(Factory, "create_poetry", return_value=mock_root_poetry):
        config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
        venv_modifier = VenvModifier(config)

        # Execute plugin
        venv_modifier.execute(cast(ConsoleCommandEvent, mock_event))

        # Verify poetry was set
        mock_command.set_poetry.assert_called_once_with(mock_root_poetry)


def test_executes_modifications_for_install_command(
    mock_event_gen: EventGenerator[InstallCommand], mock_root_poetry: MagicMock
) -> None:
    """Test venv modifier with install command."""
    mock_event = mock_event_gen(InstallCommand, True)
    mock_command = cast(MagicMock, mock_event.command)

    # Mock poetry attributes
    mock_command.poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    mock_command.poetry.disable_cache = False

    # Mock Factory.create_poetry
    with patch.object(Factory, "create_poetry", return_value=mock_root_poetry):
        config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
        venv_modifier = VenvModifier(config)

        # Execute plugin
        venv_modifier.execute(cast(ConsoleCommandEvent, mock_event))

        # Verify poetry was set
        mock_command.set_poetry.assert_called_once_with(mock_root_poetry)


def test_executes_modifications_for_other_command(
    mock_event_gen: EventGenerator[EnvCommand], mock_root_poetry: MagicMock
) -> None:
    """Test venv modifier with other command."""
    mock_event = mock_event_gen(EnvCommand, True)
    mock_command = cast(MagicMock, mock_event.command)

    # Mock poetry attributes
    mock_command.poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    mock_command.poetry.disable_cache = False

    # Mock Factory.create_poetry
    with patch.object(Factory, "create_poetry", return_value=mock_root_poetry):
        config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
        venv_modifier = VenvModifier(config)

        # Execute plugin
        venv_modifier.execute(cast(ConsoleCommandEvent, mock_event))

        # Verify poetry was set
        mock_command.set_poetry.assert_called_once_with(mock_root_poetry)
