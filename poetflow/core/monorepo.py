"""Core monorepo management functionality."""
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

from .config import Config
from .versioning import VersionManager
from .dependencies import DependencyManager
from ..types.discovery import PackageInfo


class MonoRepo:
    """Manages a monorepo"""

    def __init__(self, config: Config) -> None:
        """Initialize monorepo.

        Args:
            config: Configuration instance
        """
        self.root_path = config.root_dir
        self.config = config
        self.version_manager = VersionManager(self)
        self.dependency_manager = DependencyManager(self)
        self._packages: Dict[str, PackageInfo] = {}
        self._load_packages()

    def get_packages(self) -> List[str]:
        """Get list of package names.

        Returns:
            List of package names
        """
        return list(self._packages.keys())

    def get_package_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get package information.

        Args:
            name: Package name

        Returns:
            Package information or None if not found
        """
        pkg = self._packages.get(name)
        if not pkg:
            return None
        return {
            "name": pkg.name,
            "version": pkg.version,
            "path": str(pkg.path),
            "dependencies": list(pkg.dependencies)
        }

    def get_package(self, name: str) -> Optional[PackageInfo]:
        """Get package information.

        Args:
            name: Package name

        Returns:
            Package information or None if not found
        """
        return self._packages.get(name)

    def get_build_order(self) -> List[str]:
        """Get package build order.

        Returns:
            List of package names in build order
        """
        return self.dependency_manager.get_build_order()

    def get_package_path(self, name: str) -> Optional[Path]:
        """Get package path.

        Args:
            name: Package name

        Returns:
            Package path or None if not found
        """
        pkg = self._packages.get(name)
        return pkg.path if pkg else None

    def get_all_packages(self) -> List[str]:
        """Get all package names.

        Returns:
            List of all package names
        """
        return self.get_packages()

    def get_affected_packages(self) -> Set[str]:
        """Get packages affected by changes.

        Returns:
            Set of affected package names
        """
        affected: Set[str] = set()
        for package in self.get_packages():
            affected.add(package)
        return affected

    def get_all_dependents(self, package: str) -> Set[str]:
        """Get all packages that depend on this package.

        Args:
            package: Package name

        Returns:
            Set of dependent package names
        """
        return self.dependency_manager.get_all_dependents(package)

    def get_dependencies(self, package: str) -> Set[str]:
        """Get package dependencies.

        Args:
            package: Package name

        Returns:
            Set of dependency package names
        """
        return self.dependency_manager.get_dependencies(package)

    def _load_packages(self) -> None:
        """Load packages from disk."""
        # Implementation details...
        pass

    def execute_command(self, command: str, **kwargs: Any) -> Any:
        """Execute a command in the monorepo context.

        Args:
            command: Command name to execute
            **kwargs: Additional command arguments

        Returns:
            Command execution result

        Raises:
            ValueError: If command is not supported
        """
        if not hasattr(self, command):
            raise ValueError(f"Unknown command: {command}")
        
        method = getattr(self, command)
        return method(**kwargs)