"""Test types."""

from typing import Any, Callable, Generic, Protocol, Type, TypeVar

from cleo.events.console_command_event import ConsoleCommandEvent
from poetry.console.commands.command import Command


class MockMethod(Protocol):
    """Protocol for mock methods."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def assert_called_once_with(self, *args: Any, **kwargs: Any) -> None: ...
    @property
    def call_count(self) -> int: ...


class MockCommand(Protocol):
    """Protocol for mocked commands."""

    poetry: Any
    io: Any
    env: Any
    set_poetry: MockMethod
    set_installer: MockMethod
    set_env: MockMethod
    handle: MockMethod


class MockEvent(ConsoleCommandEvent):
    """Mock event for testing."""


T = TypeVar("T", bound=Command)


class EventGenerator(Generic[T]):
    """Event generator for testing."""

    def __init__(self, generator_func: Callable[[Type[T], bool], MockEvent]) -> None:
        """Initialize the event generator.

        Args:
            generator_func: Function that generates mock events
        """
        self._generator = generator_func

    def __call__(self, cmd_type: Type[T], is_root: bool) -> MockEvent:
        """Generate a mock event.

        Args:
            cmd_type: Type of command to mock
            is_root: Whether this is a root command

        Returns:
            A mock event
        """
        return self._generator(cmd_type, is_root)


__all__ = [
    "Command",
    "EventGenerator",
    "MockCommand",
    "MockEvent",
]
