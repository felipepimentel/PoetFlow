"""Type stubs for tomlkit interactions"""

from typing import Any, Dict, Protocol

class TOMLDocument(Dict[str, Any]):
    """Type for TOML documents"""
    pass

class api(Protocol):
    """Protocol for tomlkit.api functions"""
    @staticmethod
    def loads(string: str) -> TOMLDocument: ...
    
    @staticmethod
    def dumps(data: Dict[str, Any]) -> str: ...

def parse(string: str) -> TOMLDocument: ... 