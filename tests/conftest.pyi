"""Type stubs for test fixtures."""

from typing import Any, Protocol, TypeVar

from poetflow.types.poetry import Command as PoetryCommand

class ConsoleCommandEvent(Protocol):
    """Protocol for console command events."""

    command: Any
    io: Any

T = TypeVar("T", bound=PoetryCommand)

def mock_event_gen(
    command_cls: type[T], disable_cache: bool = False, *, io: Any = None
) -> ConsoleCommandEvent: ...
