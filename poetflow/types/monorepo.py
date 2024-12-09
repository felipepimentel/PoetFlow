"""Types for monorepo management"""

from typing import List, Optional, Protocol


class MonoRepo(Protocol):
    """Protocol defining the interface for a monorepo"""
    
    @property
    def root(self) -> str:
        """Get the root directory of the monorepo"""
        ...

    @property
    def packages(self) -> List[str]:
        """Get the list of packages in the monorepo"""
        ...


class MonorepoManager(Protocol):
    """Protocol defining the interface for monorepo management"""
    
    def get_all_packages(self) -> List[str]:
        """Get all packages in the monorepo"""
        ...

    def get_package_path(self, package: str) -> Optional[str]:
        """Get the path to a package"""
        ... 