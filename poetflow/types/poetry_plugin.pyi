"""Type stubs for Poetry plugin system."""
from typing import Protocol
from .poetry import Poetry

class ApplicationPlugin(Protocol):
    """Base plugin protocol."""
    def activate(self, poetry: Poetry) -> None: ... 