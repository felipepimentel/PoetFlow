import os
from pathlib import Path
from typing import cast
from unittest.mock import Mock, patch

import pytest
from poetry.console.commands.env_command import EnvCommand  # type: ignore
from poetry.console.commands.installer_command import InstallerCommand  # type: ignore
from poetry.installation.installer import Installer  # type: ignore
from poetry.poetry import Poetry  # type: ignore

from poetflow.config import MonorangerConfig
from poetflow.plugins.venv import VenvModifier
from tests.types import Command, EventGenerator


@pytest.mark.parametrize("disable_cache", [True, False])
def test_executes_modifications_for_env_command(
    mock_event_gen: EventGenerator[EnvCommand], disable_cache: bool
) -> None:
    mock_event = mock_event_gen(EnvCommand, disable_cache=disable_cache)
    mock_command = cast(Command, mock_event.command)
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    venv_modifier = VenvModifier(config)

    environ = os.environ.copy()
    environ.pop("VIRTUAL_ENV", None)
    with (
        patch("poetflow.plugins.venv.Factory.create_poetry", autospec=True) as mock_create_poetry,
        patch("poetflow.plugins.venv.EnvManager.create_venv", autospec=True) as mock_create_venv,
        patch.dict("os.environ", environ, clear=True),
    ):
        mock_create_poetry.return_value = Mock(spec=Poetry)
        mock_create_venv.return_value = Mock()

        venv_modifier.execute(mock_event)

        mock_create_poetry.assert_called_once()
        assert mock_create_poetry.call_args[1]["cwd"] == Path("/monorepo_root").resolve()
        assert mock_create_poetry.call_args[1]["io"] == mock_event.io
        assert mock_create_poetry.call_args[1]["disable_cache"] == disable_cache

        mock_create_venv.assert_called_once()
        assert mock_create_venv.call_args[0][0]._poetry == mock_create_poetry.return_value

        mock_command.set_env.assert_called_once()
        assert mock_command.set_env.call_args[0][0] == mock_create_venv.return_value


@pytest.mark.parametrize("disable_cache", [True, False])
def test_executes_modifications_for_installer_command(
    mock_event_gen: EventGenerator[InstallerCommand], disable_cache: bool
) -> None:
    mock_event = mock_event_gen(InstallerCommand, disable_cache=disable_cache)
    mock_command = cast(Command, mock_event.command)
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    venv_modifier = VenvModifier(config)

    environ = os.environ.copy()
    environ.pop("VIRTUAL_ENV", None)
    with (
        patch("poetflow.plugins.venv.Factory.create_poetry", autospec=True) as mock_create_poetry,
        patch("poetflow.plugins.venv.EnvManager.create_venv", autospec=True) as mock_create_venv,
        patch("poetflow.plugins.venv.Installer", autospec=True) as mock_installer_cls,
        patch.dict("os.environ", environ, clear=True),
    ):
        mock_create_poetry.return_value = Mock(spec=Poetry)
        mock_create_venv.return_value = Mock()
        mock_installer_cls.return_value = Mock(spec=Installer)

        venv_modifier.execute(mock_event)

        mock_installer_cls.assert_called_once()
        assert mock_installer_cls.call_args[0][1] == mock_create_venv.return_value
        assert mock_installer_cls.call_args[0][2] == mock_command.poetry.package
        assert mock_installer_cls.call_args[0][3] == mock_command.poetry.locker
        assert mock_installer_cls.call_args[0][4] == mock_command.poetry.pool
        assert mock_installer_cls.call_args[0][5] == mock_command.poetry.config
        assert mock_installer_cls.call_args[1]["disable_cache"] == mock_command.poetry.disable_cache

        mock_command.set_installer.assert_called_once()
        assert mock_command.set_installer.call_args[0][0] == mock_installer_cls.return_value


@pytest.mark.parametrize("disable_cache", [True, False])
def test_does_not_activate_venv_if_already_in_venv(
    mock_event_gen: EventGenerator[EnvCommand], disable_cache: bool
) -> None:
    mock_event = mock_event_gen(EnvCommand, disable_cache=disable_cache)
    mock_command = cast(Command, mock_event.command)
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    venv_modifier = VenvModifier(config)

    environ = os.environ.copy()
    environ["VIRTUAL_ENV"] = "/some/venv"
    with (
        patch("poetflow.plugins.venv.Factory.create_poetry", autospec=True) as mock_create_poetry,
        patch("poetflow.plugins.venv.EnvManager.create_venv", autospec=True) as mock_create_venv,
        patch.dict("os.environ", environ, clear=True),
    ):
        venv_modifier.execute(mock_event)

        mock_create_poetry.assert_not_called()
        mock_create_venv.assert_not_called()
        mock_command.set_env.assert_not_called()
