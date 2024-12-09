"""Type definitions for tests."""
from typing import Any, Callable, Protocol, TypeVar, Union

from poetry.console.commands.add import AddCommand  # type: ignore
from poetry.console.commands.build import BuildCommand  # type: ignore
from poetry.console.commands.env_command import EnvCommand  # type: ignore
from poetry.console.commands.install import InstallCommand  # type: ignore
from poetry.console.commands.lock import LockCommand  # type: ignore
from poetry.console.commands.remove import RemoveCommand  # type: ignore
from poetry.console.commands.update import UpdateCommand  # type: ignore
from cleo.events.console_command_event import ConsoleCommandEvent  # type: ignore


class MockCallable(Protocol):
    """Protocol for mock callable objects."""
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    assert_called_once: Callable[[], None]
    assert_called_once_with: Callable[..., None]
    assert_not_called: Callable[[], None]
    call_args: tuple[tuple[Any, ...], dict[str, Any]]


class Poetry(Protocol):
    """Protocol for Poetry instance."""
    package: Any
    locker: Any
    pool: Any
    config: Any
    disable_cache: bool
    pyproject_path: Any


class Command(Protocol):
    """Protocol for Poetry commands."""
    poetry: Poetry
    io: Any
    env: Any
    set_poetry: MockCallable
    set_installer: MockCallable
    set_env: MockCallable


class DependencyInfo(Protocol):
    """Protocol for dependency information."""
    name: str
    pretty_constraint: str


SupportedCommand = Union[
    AddCommand, RemoveCommand, BuildCommand, EnvCommand,
    LockCommand, InstallCommand, UpdateCommand
]

T = TypeVar("T", bound=SupportedCommand)

# Define EventGenerator after T is defined
EventGenerator = Callable[[type[T], bool], ConsoleCommandEvent]

__all__ = [
    "Command",
    "ConsoleCommandEvent",
    "DependencyInfo",
    "EventGenerator",
    "MockCallable",
    "Poetry",
    "SupportedCommand",
    "T",
] 