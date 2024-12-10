"""Tests for PathRewriter."""

from pathlib import Path
from typing import cast
from unittest.mock import Mock

from poetry.console.commands.build import BuildCommand
from poetry.core.packages.directory_dependency import DirectoryDependency

from poetflow.plugins.path import CommandEvent, PathRewriter
from poetflow.types.config import MonorangerConfig
from tests.types import EventGenerator


def test_executes_modifications_for_build_command(
    mock_event_gen: EventGenerator[BuildCommand],
) -> None:
    """Test path rewriter with build command."""
    # Set up mocks
    poetry_mock = Mock()
    poetry_mock.file = Mock()
    poetry_mock.file.parent = Path("/fake/path")
    poetry_mock.package = Mock()

    # Create dependency group mock
    mock_dep_group = Mock()
    mock_dep = DirectoryDependency("packageB", Path("../packageB"), develop=True)
    mock_dep_group.dependencies = {"packageB": mock_dep}
    poetry_mock.package.dependency_groups = {"main": mock_dep_group}

    # Create mock event
    mock_event = mock_event_gen(BuildCommand, True)
    mock_command = cast(Mock, mock_event.command)
    mock_command.poetry = poetry_mock

    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"))
    path_rewriter = PathRewriter(config)

    # Execute plugin
    path_rewriter.execute(cast(CommandEvent, mock_event))

    # Verify dependency was rewritten
    assert str(mock_dep.path) == "packageB"
