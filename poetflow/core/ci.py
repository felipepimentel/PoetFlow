"""CI/CD functionality for the monorepo."""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set, cast

from ..core.monorepo import MonoRepo
from ..core.dependencies import DependencyManager


class CIManager:
    """Manages CI/CD operations."""

    def __init__(self, monorepo: MonoRepo):
        """Initialize CI manager.

        Args:
            monorepo: MonoRepo instance
        """
        self.monorepo = monorepo
        self.dependency_manager = DependencyManager(monorepo)

    def _get_changed_files(self) -> Set[Path]:
        """Get list of files changed since last commit.

        Returns:
            Set of changed file paths
        """
        try:
            # Get changed files from git
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~1"], capture_output=True, text=True, check=True
            )
            return {Path(file) for file in result.stdout.splitlines() if file.strip()}
        except subprocess.CalledProcessError:
            # If git command fails (e.g., first commit), return all files
            return {
                path for path in Path(".").rglob("*") if path.is_file() and ".git" not in path.parts
            }

    def get_affected_packages_from_changes(self) -> Set[str]:
        """Get packages affected by recent changes.

        Returns:
            Set of package names that were affected
        """
        changed_files = self._get_changed_files()
        return self.get_affected_packages(changed_files)

    def run_tests(self, package: Optional[str] = None) -> bool:
        """Run tests for one or all packages.

        Args:
            package: Optional package name to test

        Returns:
            True if all tests pass
        """
        packages: List[str] = [package] if package else list(self.monorepo.get_packages())
        success = True

        for pkg in packages:
            pkg_info = self.monorepo.get_package_info(pkg)
            if not pkg_info:
                continue

            pkg_path = Path(cast(Dict[str, str], pkg_info)["path"])
            try:
                subprocess.run(["poetry", "run", "pytest"], cwd=pkg_path, check=True)
            except subprocess.CalledProcessError:
                success = False

        return success

    def run_ci(self) -> bool:
        """Run CI pipeline for affected packages.

        Returns:
            True if CI passes
        """
        # Get affected packages
        affected = self.get_affected_packages_from_changes()
        packages = list(affected)

        if not packages:
            return True

        # Run tests
        return self.run_tests(packages[0])

    def get_affected_packages(self, changed_files: Set[Path]) -> Set[str]:
        """Get all packages affected by changes

        Args:
            changed_files: Set of changed file paths

        Returns:
            Set of package names that need to be rebuilt
        """
        directly_affected = self._get_directly_affected_packages(changed_files)
        all_affected: Set[str] = set()

        for package in directly_affected:
            all_affected.update(self.dependency_manager.get_all_dependents(package))

        return all_affected | directly_affected

    def _get_directly_affected_packages(self, changed_files: Set[Path]) -> Set[str]:
        """Get packages directly affected by file changes

        Args:
            changed_files: Set of changed file paths

        Returns:
            Set of package names that contain changed files
        """
        result: Set[str] = set()
        packages = self.monorepo.get_packages()

        for file_path in changed_files:
            for package in packages:
                pkg_info = self.monorepo.get_package_info(package)
                if not pkg_info:
                    continue
                pkg_path = Path(cast(Dict[str, str], pkg_info)["path"])
                if pkg_path in file_path.parents:
                    result.add(package)
                    break

        return result
