"""Poetry plugin for PoetFlow."""

from pathlib import Path
from typing import Any, Optional

from poetry.plugins.application_plugin import ApplicationPlugin  # type: ignore

from .types.config import MonorangerConfig


class Monoranger(ApplicationPlugin):
    """Poetry plugin for monorepo management."""

    def __init__(self) -> None:
        self.plugin_conf: Optional[MonorangerConfig] = None

    def activate(self, application: Any) -> None:
        """Activate the plugin.

        Args:
            application: Poetry application instance
        """
        config_data = application.pyproject.data.get("tool", {}).get("poetry-monoranger-plugin", {})
        if not config_data:
            return

        enabled = config_data.get("enabled", False)
        if not enabled:
            return

        monorepo_root = Path(config_data.get("monorepo_root", ".."))
        packages_dir = config_data.get("packages_dir")

        self.plugin_conf = MonorangerConfig(
            enabled=enabled,
            monorepo_root=monorepo_root,
            packages_dir=packages_dir,
        )

        # Register event listeners
        application.event_dispatcher.add_listener("pre_command", self.pre_command)
        application.event_dispatcher.add_listener("post_command", self.post_command)

    def pre_command(self, event: Any) -> None:
        """Handle pre-command events.

        Args:
            event: Command event
        """
        if not self.plugin_conf or not self.plugin_conf.enabled:
            return

    def post_command(self, event: Any) -> None:
        """Handle post-command events.

        Args:
            event: Command event
        """
        if not self.plugin_conf or not self.plugin_conf.enabled:
            return

    def console_command_event_listener(self, event: Any, event_name: str, dispatcher: Any) -> None:
        """Handle console command events.

        Args:
            event: Command event
            event_name: Name of the event
            dispatcher: Event dispatcher
        """
        if not self.plugin_conf or not self.plugin_conf.enabled:
            return 