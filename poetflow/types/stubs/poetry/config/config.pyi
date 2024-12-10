"""Type stubs for poetry.config.config"""

from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """Poetry configuration."""
    @classmethod
    def create(cls, reload: bool = False) -> "Config": ...
    def get(self, setting_name: str, default: Any = None) -> Any: ...
    def set(self, setting_name: str, value: Any) -> None: ...
    def merge(self, config: Dict[str, Any]) -> None: ...
    def remove(self, setting_name: str) -> None: ...
    def all(self) -> Dict[str, Any]: ...
    @property
    def repository_cache_directory(self) -> Path: ...
    @property
    def virtualenvs_path(self) -> Path: ...
    @property
    def installer_max_workers(self) -> int: ...
    @property
    def config_file(self) -> Optional[Path]: ...