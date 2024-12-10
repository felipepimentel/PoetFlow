"""Type stubs for poetry.console.command"""

from typing import Any

from cleo.commands.command import Command as BaseCommand
from poetry.poetry import Poetry

class Command(BaseCommand):
    """Base command stub."""
    @property
    def poetry(self) -> Poetry: ...
    def handle(self) -> int: ...
    def set_poetry(self, poetry: Poetry) -> None: ...
    def set_installer(self, installer: Any) -> None: ...
    def set_env(self, env: Any) -> None: ...
    def set_manager(self, manager: Any) -> None: ...