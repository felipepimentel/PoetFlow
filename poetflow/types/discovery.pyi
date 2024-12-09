"""Type stubs for package discovery."""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

@dataclass
class PackageInfo:
    """Information about a package"""
    name: str
    version: str
    path: Path
    dependencies: Set[str]

class PackageDiscovery:
    """Package discovery functionality"""
    def discover_packages(self) -> List[PackageInfo]: ...
    def analyze_dependencies(self, packages: List[PackageInfo]) -> Dict[str, Set[str]]: ... 