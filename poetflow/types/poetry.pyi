from typing import Any, List, Optional, Protocol
from pathlib import Path
from cleo.io.io import IO

class Package:
    name: str
    version: str

class Poetry:
    package: Package
    file: Any
    locker: Any
    pool: Any
    config: Any
    pyproject_path: Path
    disable_cache: bool

class Config:
    @classmethod
    def create(cls, reload: bool = False) -> "Config": ...

class Factory:
    @staticmethod
    def create_poetry(
        cwd: Path,
        io: Optional[IO] = None,
        disable_cache: bool = False
    ) -> Poetry: ...

class Command(Protocol):
    """Base command protocol"""
    poetry: Poetry
    io: IO

    def handle(self) -> int: ...
    def set_poetry(self, poetry: Poetry) -> None: ...

class AddCommand(Command): ...
class RemoveCommand(Command): ...
class BuildCommand(Command): ...
class LockCommand(Command): ...
class InstallCommand(Command): ...
class UpdateCommand(Command): ...
class EnvCommand(Command): ...
class SelfCommand(EnvCommand): ...

class Installer:
    def __init__(
        self,
        io: IO,
        env: Any,
        package: Package,
        locker: Any,
        pool: Any,
        config: Any,
        disable_cache: bool = False
    ) -> None: ...
    
    def run(self) -> int: ...
    def dry_run(self, dry_run: bool) -> None: ...
    def verbose(self, verbose: bool) -> None: ...
    def update(self, update: bool) -> None: ...
    def whitelist(self, packages: List[str]) -> None: ...
    def execute_operations(self, execute: bool) -> None: ...

class Application:
    poetry: Poetry
    event_dispatcher: Any
    
    def add_event_listener(self, event: str, listener: Any) -> None: ...

class ApplicationPlugin:
    def activate(self, application: Application) -> None: ... 