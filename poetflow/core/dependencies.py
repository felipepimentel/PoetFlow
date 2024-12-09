"""Copyright (C) 2024 felipepimentel plc

This module handles dependency management for packages in the monorepo.
"""

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, TypeVar, cast

import tomlkit
from tomlkit.items import Table

from poetflow.core.exceptions import PackageError
from poetflow.types import MonoRepo

T = TypeVar("T")


class DependencyManager:
    """Manages dependencies between packages"""

    def __init__(self, monorepo: MonoRepo) -> None:
        self.monorepo = monorepo
        self._dependencies: Dict[str, Set[str]] = {}
        self._dependents: Dict[str, Set[str]] = {}
        self._load_dependencies()

    def _load_dependencies(self) -> None:
        """Load dependencies from pyproject.toml files"""
        for package in self.monorepo.get_packages():
            pkg_info = self.monorepo.get_package_info(package)
            if not pkg_info:
                continue

            pkg_path = Path(cast(str, pkg_info["path"]))
            pyproject_path = pkg_path / "pyproject.toml"

            with open(pyproject_path) as f:
                pyproject = tomlkit.parse(f.read())

            deps: Set[str] = set()
            if "tool" in pyproject:
                tool = cast(Table, pyproject["tool"])
                if "poetry" in tool:
                    poetry_config = cast(Table, tool["poetry"])
                    if "dependencies" in poetry_config:
                        dependencies = cast(Dict[str, Any], poetry_config["dependencies"])
                        for name in dependencies:
                            if name in self.monorepo.get_packages():
                                deps.add(str(name))

            self._dependencies[package] = deps
            for dep_name in deps:
                if dep_name not in self._dependents:
                    self._dependents[dep_name] = set()
                self._dependents[dep_name].add(package)

    def get_dependencies(self, package: str) -> Set[str]:
        """Get direct dependencies of a package

        Args:
            package: Package name

        Returns:
            Set of package names
        """
        return self._dependencies.get(package, set())

    def get_dependents(self, package: str) -> Set[str]:
        """Get direct dependents of a package

        Args:
            package: Package name

        Returns:
            Set of package names
        """
        return self._dependents.get(package, set())

    def get_build_order(self) -> List[str]:
        """Get correct build order for all packages.

        Returns:
            List of package names in build order

        Raises:
            PackageError: If circular dependency is detected
        """
        result: List[str] = []
        in_degree: Dict[str, int] = defaultdict(int)
        packages = self.monorepo.get_packages()

        # Calculate in-degree for each package
        for package in packages:
            for _ in self.get_dependencies(package):
                in_degree[package] += 1

        # Start with packages that have no dependencies
        queue = [pkg for pkg in packages if in_degree[pkg] == 0]

        while queue:
            package = queue.pop(0)
            result.append(package)

            # Reduce in-degree of dependents
            for dependent in self.get_dependents(package):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(packages):
            raise PackageError("Circular dependency detected")

        return result

    def get_all_dependents(self, package: str) -> Set[str]:
        """Get all packages that depend on this package (directly or indirectly)

        Args:
            package: Package name

        Returns:
            Set of package names that depend on this package
        """
        result: Set[str] = set()
        to_process = {package}

        while to_process:
            current = to_process.pop()
            direct_dependents = self.get_dependents(current)

            new_dependents = direct_dependents - result
            result.update(new_dependents)
            to_process.update(new_dependents)

        return result

    def get_affected_packages(self) -> Set[str]:
        """Get packages affected by changes.

        Returns:
            Set of affected package names
        """
        affected: Set[str] = set()
        for package in self.monorepo.get_packages():
            # Implementation details...
            # This is just a placeholder - you'll need to implement the actual logic
            affected.add(package)
        return affected
