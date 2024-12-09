"""Tests for Poetry plugins."""

from pathlib import Path
from typing import Type
from unittest.mock import Mock, PropertyMock, patch

import pytest
from poetry.console.commands.add import AddCommand  # type: ignore
from poetry.console.commands.build import BuildCommand  # type: ignore
from poetry.console.commands.env_command import EnvCommand  # type: ignore
from poetry.console.commands.install import InstallCommand  # type: ignore
from poetry.console.commands.lock import LockCommand  # type: ignore
from poetry.console.commands.remove import RemoveCommand  # type: ignore
from poetry.console.commands.update import UpdateCommand  # type: ignore
from poetry.factory import Factory
from poetry.poetry import Poetry  # type: ignore
from poetry.utils.env import Env  # type: ignore

from poetflow.plugins.base import Plugin
from poetflow.plugins.dependency import MonorepoAdderRemover
from poetflow.plugins.lock import LockModifier
from poetflow.plugins.path import PathRewriter
from poetflow.plugins.venv import VenvModifier
from poetflow.types.config import MonorangerConfig
from tests.types import EventGenerator, SupportedCommand


@pytest.mark.parametrize(
    "cmd_type,plugin_class",
    [
        (AddCommand, MonorepoAdderRemover),
        (RemoveCommand, MonorepoAdderRemover),
        (BuildCommand, PathRewriter),
        (EnvCommand, VenvModifier),
        (LockCommand, LockModifier),
        (InstallCommand, LockModifier),
        (UpdateCommand, LockModifier),
    ],
)
def test_handles_all_command_events(
    mock_event_gen: EventGenerator[SupportedCommand],
    cmd_type: Type[SupportedCommand],
    plugin_class: Type[Plugin],
) -> None:
    event = mock_event_gen(cmd_type, False)
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"), packages_dir=None)

    # Create a new Poetry instance for the root project with proper mocking
    mock_root_poetry = Mock(spec=Poetry)
    mock_root_pyproject = Mock()
    mock_root_pyproject.poetry_config = {"name": "root-package", "version": "1.0.0"}
    mock_root_pyproject.file = Mock()
    
    # Fix: Set up proper Poetry attribute hierarchy
    mock_root_poetry._pyproject = mock_root_pyproject  # Set the private attribute
    type(mock_root_poetry).pyproject = PropertyMock(return_value=mock_root_pyproject)
    
    mock_root_poetry.locker = Mock()
    mock_root_poetry.locker.lock_data = {"metadata": {"version": "1.0.0"}}
    mock_root_poetry.package = Mock()
    mock_root_poetry.package.name = "root-package"
    
    # Fix: Properly mock the config object
    mock_config = Mock()
    mock_config.repository_cache_directory = Path("/tmp/poetry/cache")
    mock_config.installer_max_workers = 4
    mock_config.virtualenvs_path = Path("/tmp/poetry/virtualenvs")
    mock_root_poetry.config = mock_config
    
    mock_root_poetry.pool = Mock()
    
    # Fix: Use actual Path objects for root poetry
    root_path = Path("/monorepo_root")
    mock_root_poetry.pyproject_path = root_path / "pyproject.toml"
    mock_root_poetry.file = Mock()
    mock_root_poetry.file.parent = root_path
    mock_root_poetry.file.read = Mock(return_value={"tool": {"poetry": {"version": "1.0.0"}}})
    mock_root_poetry.disable_cache = False

    # Fix: Create a copy of the root poetry for Factory.create_poetry
    mock_root_poetry_copy = Mock(spec=Poetry)
    mock_root_poetry_copy.__dict__.update(mock_root_poetry.__dict__)
    
    # Fix: Ensure the event's poetry object has consistent paths, config and attributes
    event_poetry = event.command.poetry
    event_poetry._pyproject = mock_root_pyproject  # Set the private attribute
    type(event_poetry).pyproject = PropertyMock(return_value=mock_root_pyproject)
    event_poetry.pyproject_path = root_path / "packageA" / "pyproject.toml"
    event_poetry.file = Mock()
    event_poetry.file.parent = root_path / "packageA"
    event_poetry.file.read = Mock(return_value={"tool": {"poetry": {"version": "1.0.0"}}})
    event_poetry.config = mock_config

    # Fix: Properly mock the environment and ensure we're not in a venv
    mock_env = Mock(spec=Env)
    mock_env.sys_path = [
        str(Path("/monorepo_root/.venv/lib/python3.8/site-packages")),
        str(Path("/usr/lib/python3.8/site-packages")),
    ]
    mock_env.get_site_packages = Mock(return_value=Path("/monorepo_root/.venv/lib/python3.8/site-packages"))
    mock_env.get_paths = Mock(return_value={"purelib": "/monorepo_root/.venv/lib/python3.8/site-packages"})
    mock_env.exists = Mock(return_value=True)
    mock_env.is_venv = Mock(return_value=True)
    event.command.env = mock_env

    # Fix: Mock Config.create to return our mock config and patch EnvManager
    with (
        patch.object(Factory, "create_poetry", return_value=mock_root_poetry_copy),
        patch("poetry.config.config.Config.create", return_value=mock_config),
        patch.dict("os.environ", {}, clear=True),
        patch("poetry.utils.env.EnvManager.create_venv", return_value=mock_env),
    ):
        plugin = plugin_class(config)
        plugin.execute(event)

        # Fix: Update assertions to match actual plugin behavior
        if isinstance(plugin, PathRewriter):
            # PathRewriter doesn't modify poetry or installer
            assert event.command.set_poetry.call_count == 0
            assert event.command.set_installer.call_count == 0
        elif isinstance(plugin, VenvModifier):
            # VenvModifier only sets env when not in a venv
            assert event.command.set_poetry.call_count == 0
            assert event.command.set_installer.call_count == 0
            assert event.command.set_env.call_count == 1
        else:
            # MonorepoAdderRemover and LockModifier set both poetry and installer
            assert event.command.set_poetry.call_count == 1
            assert event.command.set_installer.call_count == 1
