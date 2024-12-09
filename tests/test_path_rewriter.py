import copy
from pathlib import Path
from typing import cast
from unittest.mock import Mock, patch

import pytest
from poetry.console.commands.build import BuildCommand  # type: ignore
from poetry.core.packages.directory_dependency import DirectoryDependency  # type: ignore
from poetry.core.pyproject.toml import PyProjectTOML  # type: ignore

from poetflow.config import MonorangerConfig
from poetflow.plugins.path import PathRewriter
from tests.types import Command, DependencyInfo, EventGenerator


@pytest.mark.parametrize("disable_cache", [True, False])
def test_executes_path_rewriting_for_build_command(
    mock_event_gen: EventGenerator[BuildCommand], disable_cache: bool
) -> None:
    mock_event = mock_event_gen(BuildCommand, disable_cache=disable_cache)
    mock_command = cast(Command, mock_event.command)
    config = MonorangerConfig(enabled=True, monorepo_root=Path("../"), version_rewrite_rule="==")
    path_rewriter = PathRewriter(config)

    original_dependencies = copy.deepcopy(mock_command.poetry.package.dependency_group.return_value.dependencies)

    with patch("poetflow.plugins.path.PathRewriter._get_dependency_pyproject", autospec=True) as mock_get_dep:
        mock_get_dep.return_value = Mock(spec=PyProjectTOML)
        mock_get_dep.return_value.poetry_config = {"version": "0.1.0", "name": "packageB"}

        path_rewriter.execute(mock_event)

    new_dependencies = mock_command.poetry.package.dependency_group.return_value

    assert len(new_dependencies.dependencies) == len(original_dependencies)
    # sort the dependencies by name to ensure they are in the same order
    original_dependencies = sorted(original_dependencies, key=lambda x: x.name)  # type: ignore
    new_dependencies = sorted(new_dependencies.dependencies, key=lambda x: x.name)  # type: ignore
    for i, dep in enumerate(new_dependencies):
        dep_info = cast(DependencyInfo, dep)
        orig_info = cast(DependencyInfo, original_dependencies[i])
        assert dep_info.name == orig_info.name
        if isinstance(original_dependencies[i], DirectoryDependency):
            assert dep_info.pretty_constraint == "0.1.0"
        else:
            assert dep_info.pretty_constraint == orig_info.pretty_constraint
