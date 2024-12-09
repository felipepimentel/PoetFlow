from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from poetry.console.commands.add import AddCommand  # type: ignore
from poetry.console.commands.build import BuildCommand  # type: ignore
from poetry.console.commands.env_command import EnvCommand  # type: ignore
from poetry.console.commands.install import InstallCommand  # type: ignore
from poetry.console.commands.lock import LockCommand  # type: ignore
from poetry.console.commands.remove import RemoveCommand  # type: ignore
from poetry.console.commands.update import UpdateCommand  # type: ignore

from poetflow.config import MonorangerConfig
from poetflow.plugin import Monoranger
from tests.types import EventGenerator, SupportedCommand


@pytest.mark.parametrize(
    "cmd_type",
    [
        AddCommand,
        RemoveCommand,
        BuildCommand,
        EnvCommand,
        LockCommand,
        InstallCommand,
        UpdateCommand,
    ],
)
def test_handles_all_command_events(
    mock_event_gen: EventGenerator[SupportedCommand], cmd_type: type[SupportedCommand]
) -> None:
    cmd_to_patch = {
        AddCommand: "poetflow.plugins.dependency.MonorepoAdderRemover",
        RemoveCommand: "poetflow.plugins.dependency.MonorepoAdderRemover",
        BuildCommand: "poetflow.plugins.path.PathRewriter",
        EnvCommand: "poetflow.plugins.venv.VenvModifier",
        LockCommand: "poetflow.plugins.lock.LockModifier",
        InstallCommand: "poetflow.plugins.lock.LockModifier",
        UpdateCommand: "poetflow.plugins.lock.LockModifier",
    }

    event = mock_event_gen(cmd_type, disable_cache=False)
    plugin = Monoranger()
    plugin.plugin_conf = MonorangerConfig(
        enabled=True, monorepo_root=Path("../"), packages_dir=None
    )

    with patch(cmd_to_patch[cmd_type]) as mock_class:
        mock_instance = Mock()
        mock_instance.execute = Mock()
        mock_class.return_value = mock_instance

        plugin.console_command_event_listener(event, "console.command", Mock())

        mock_class.assert_called_once_with(plugin.plugin_conf)
        mock_instance.execute.assert_called_once_with(event)
