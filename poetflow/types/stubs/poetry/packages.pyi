"""Type stubs for poetry.packages"""

from typing import Any, List, Optional

class Package:
    """Poetry package."""
    def __init__(
        self,
        name: str,
        version: str,
        pretty_version: Optional[str] = None,
        source_type: Optional[str] = None,
        source_url: Optional[str] = None,
        source_reference: Optional[str] = None,
        source_resolved_reference: Optional[str] = None,
        features: Optional[List[str]] = None,
        optional: bool = False,
    ) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def version(self) -> str: ...
    @property
    def pretty_version(self) -> str: ...
    @property
    def source_type(self) -> Optional[str]: ...
    @property
    def source_url(self) -> Optional[str]: ...
    @property
    def source_reference(self) -> Optional[str]: ...
    @property
    def source_resolved_reference(self) -> Optional[str]: ...
    @property
    def features(self) -> List[str]: ...
    @property
    def optional(self) -> bool: ...
    @property
    def python_versions(self) -> str: ...
    @property
    def python_constraint(self) -> Any: ...
    @property
    def platform(self) -> Optional[str]: ...
    @property
    def marker(self) -> Optional[str]: ...
    @property
    def extras(self) -> List[str]: ...
    @property
    def requires(self) -> List[Any]: ...
    @property
    def dev_requires(self) -> List[Any]: ...
    @property
    def all_requires(self) -> List[Any]: ...
