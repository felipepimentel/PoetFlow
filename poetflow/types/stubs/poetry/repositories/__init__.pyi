"""Type stubs for poetry.repositories"""

from typing import Any, Dict, List, Optional

from ..packages import Package

class Repository:
    """Poetry package repository."""
    def __init__(self, name: str = "repo") -> None: ...
    def has_package(self, package: Package) -> bool: ...
    def package(self, name: str, version: str) -> Optional[Package]: ...
    def find_packages(self, dependency: Any) -> List[Package]: ...
    def search(self, query: str) -> List[Package]: ...
    def get_package_entries(self) -> Dict[str, List[Package]]: ...
    def add_package(self, package: Package) -> None: ...
    def remove_package(self, package: Package) -> None: ...
