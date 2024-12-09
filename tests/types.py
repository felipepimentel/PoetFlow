"""Type definitions for tests."""

from typing import Any, Callable, Protocol, Tuple, Type, TypeVar, Union, runtime_checkable

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_terminate_event import ConsoleTerminateEvent

from poetflow.types.poetry_commands import (
    AddCommand,
    BuildCommand,
    Command,
    EnvCommand,
    InstallCommand,
    LockCommand,
    RemoveCommand,
    UpdateCommand,
)

T = TypeVar("T", bound=Command)


class MockCallable(Protocol):
    """Protocol for mock callable objects."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def assert_called_once(self) -> None: ...
    def assert_called_once_with(self, *args: Any, **kwargs: Any) -> None: ...

    call_args: Tuple[Tuple[Any, ...], dict[str, Any]]
    call_count: int


class MockCommand(Protocol):
    """Protocol for mocked commands."""

    poetry: Any
    io: Any
    env: Any
    set_poetry: MockCallable
    set_installer: MockCallable
    set_env: MockCallable


class DependencyInfo(Protocol):
    """Protocol for dependency information."""

    name: str
    pretty_constraint: str


@runtime_checkable
class MockEvent(Protocol):
    """Protocol for mocked events."""

    command: MockCommand
    io: Any

    def set_exit_code(self, code: int) -> None: ...
    def is_debug(self) -> bool: ...
    def is_quiet(self) -> bool: ...
    def is_verbose(self) -> bool: ...
    def has_terminated(self) -> bool: ...
    @property
    def output(self) -> str: ...
    @property
    def error_output(self) -> str: ...


SupportedCommand = Union[
    AddCommand,
    RemoveCommand,
    BuildCommand,
    EnvCommand,
    LockCommand,
    InstallCommand,
    UpdateCommand,
]

EventGenerator = Callable[[Type[T], bool], MockEvent]

__all__ = [
    "Command",
    "ConsoleCommandEvent",
    "ConsoleTerminateEvent",
    "DependencyInfo",
    "EventGenerator",
    "MockCallable",
    "MockCommand",
    "MockEvent",
    "SupportedCommand",
    "T",
]
