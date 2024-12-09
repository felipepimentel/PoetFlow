"""Path rewriter plugin for Poetry."""

from typing import Any, Protocol

from poetry.core.packages.dependency import Dependency  # type: ignore
from poetry.core.packages.directory_dependency import DirectoryDependency  # type: ignore

from poetflow.types.config import MonorangerConfig


class CommandEvent(Protocol):
    """Protocol for command events."""
    command: Any
    io: Any


class PathRewriter:
    """Rewrites paths in Poetry dependencies."""

    def __init__(self, config: MonorangerConfig) -> None:
        self.config = config

    def execute(self, event: CommandEvent) -> None:
        """Execute the plugin.

        Args:
            event: The command event
        """
        if not self.config.enabled:
            return

        # Implementação aqui... 