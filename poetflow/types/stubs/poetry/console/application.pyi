"""Type stubs for poetry.console.application"""

from cleo.commands.command import Command
from cleo.events.console_command_event import ConsoleCommandEvent

class Application:
    def __init__(self) -> None: ...
    def handle_command_event(self, event: ConsoleCommandEvent) -> None: ...
    def get_command(self, name: str) -> Command: ...
