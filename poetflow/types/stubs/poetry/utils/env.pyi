"""Type stubs for poetry.utils.env"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from poetry.poetry import Poetry

class Env:
    """Poetry environment."""
    def __init__(self, path: Optional[Union[str, Path]] = None) -> None: ...
    def get_python_version(self) -> str: ...
    def get_pip_version(self) -> str: ...
    def get_python_implementation(self) -> str: ...
    def get_python_path(self) -> str: ...
    def get_site_packages(self) -> Path: ...
    def get_paths(self) -> Dict[str, str]: ...
    def get_supported_tags(self) -> List[str]: ...
    def get_marker_env(self) -> Dict[str, Any]: ...
    def get_version_info(self) -> tuple[int, ...]: ...
    def is_venv(self) -> bool: ...
    def is_sane(self) -> bool: ...
    def get_base_prefix(self) -> str: ...
    def exists(self) -> bool: ...

class EnvManager:
    """Poetry environment manager."""
    def __init__(self, poetry: Poetry, io: Optional[Any] = None) -> None: ...
    def create_venv(self) -> Env: ...
    def get(self) -> Env: ...
    def list(self) -> List[Env]: ...
    def remove(self, python: str) -> None: ...
    def build_venv(self, python: str) -> Env: ...
