"""Main application class for PoetFlow."""

from typing import Any, Mapping, Optional, TypeVar

from .core.config import Config
from .core.logging import setup_logging
from .core.monorepo import MonoRepo

T = TypeVar("T")


class Application:
    """Main application class that orchestrates PoetFlow's functionality."""

    def __init__(self, config: Optional[Mapping[str, Any]] = None):
        """Initialize the PoetFlow application.

        Args:
            config: Optional configuration dictionary
        """
        setup_logging()
        self.config = Config.from_dict(dict(config or {}))
        self.monorepo = MonoRepo(self.config)

    def run(self, command: str, **kwargs: Any) -> Any:
        """Run a PoetFlow command.

        Args:
            command: Command name to execute
            **kwargs: Command arguments

        Returns:
            Command execution result
        """
        return self.monorepo.execute_command(command, **kwargs)
