"""Tests for Plugin."""

from pathlib import Path
from typing import Type, cast
from unittest.mock import MagicMock

from cleo.events.console_command_event import ConsoleCommandEvent
from poetry.console.commands.command import Command

from poetflow.plugins.venv import VenvModifier
from poetflow.types.config import MonorangerConfig
from tests.types import EventGenerator


def test_handles_all_command_events(
    mock_event_gen: EventGenerator[Command],
    cmd_type: Type[Command],
) -> None:
    """Test plugin handles all command events."""
    # Create mock event
    mock_event = mock_event_gen(cmd_type, True)
    mock_command = cast(MagicMock, mock_event.command)

    # Mock poetry attributes
    mock_command.poetry = MagicMock()
    mock_command.poetry.file = MagicMock()
    mock_command.poetry.file.parent = Path("/fake/path")
    mock_command.poetry.pyproject_path = Path("/fake/path/pyproject.toml")
    mock_command.poetry.disable_cache = False

    # Create plugin instance
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    plugin = VenvModifier(config)

    # Execute plugin
    plugin.execute(cast(ConsoleCommandEvent, mock_event))

    # Since this is a base Command type, no modifications should be made
    assert not mock_command.set_poetry.called
