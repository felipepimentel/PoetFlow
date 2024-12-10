"""Test fixtures."""

from typing import TypeVar, cast
from unittest.mock import MagicMock, create_autospec

import pytest
from poetry.console.commands.command import Command
from poetry.poetry import Poetry

from tests.types import EventGenerator, MockCommand, MockEvent

T = TypeVar("T", bound=Command)


@pytest.fixture
def mock_command() -> MockCommand:
    command = MagicMock()
    command.poetry = MagicMock()
    command.io = MagicMock()
    command.env = MagicMock()
    command.set_poetry = MagicMock()
    command.set_installer = MagicMock()
    command.set_env = MagicMock()
    command.handle = MagicMock()
    return cast(MockCommand, command)


@pytest.fixture
def mock_event(mock_command: MockCommand) -> MockEvent:
    event = MagicMock()
    event.command = mock_command
    event.io = mock_command.io
    return cast(MockEvent, event)


@pytest.fixture
def mock_root_poetry() -> MagicMock:
    """Create a mock root poetry instance."""
    return MagicMock(spec=Poetry)


@pytest.fixture
def mock_event_gen() -> EventGenerator[Command]:
    """Create a mock event generator."""

    def _gen(cmd_type: type[Command], is_root: bool = False) -> MockEvent:
        event = MagicMock()
        command = create_autospec(cmd_type, instance=True)
        command.poetry = MagicMock()
        command.io = MagicMock()
        command.env = MagicMock()
        command.set_poetry = MagicMock()
        command.set_installer = MagicMock()
        command.set_env = MagicMock()
        command.handle = MagicMock()
        event.command = command
        event.io = command.io
        return cast(MockEvent, event)

    return EventGenerator[Command](_gen)


@pytest.fixture
def cmd_type() -> type[Command]:
    """Return the Command class."""
    return Command
