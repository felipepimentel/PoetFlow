"""Type stubs for tomlkit"""

from typing import Any, Dict, Iterator, List, Mapping, Optional, TypeVar, Union, overload

T = TypeVar("T")
KeyType = str
ValueType = Union[str, int, float, bool, Dict[str, Any], List[Any], "Item", "Table"]

class Item:
    """Base class for TOML items."""

    pass

class Table(Dict[KeyType, ValueType]):
    """TOML table."""
    def add(self, key: KeyType, value: ValueType) -> None: ...
    @overload
    def get(self, key: KeyType) -> Optional[ValueType]: ...
    @overload
    def get(self, key: KeyType, default: T) -> Union[ValueType, T]: ...

def parse(string: str) -> TOMLDocument: ...
def dumps(
    data: Union[TOMLDocument, Mapping[KeyType, ValueType]], sort_keys: bool = False
) -> str: ...
def loads(string: str) -> Dict[KeyType, ValueType]: ...
def table() -> Table: ...

class TOMLDocument(Mapping[KeyType, ValueType]):
    def __init__(self) -> None: ...
    @overload
    def get(self, key: KeyType) -> Optional[ValueType]: ...
    @overload
    def get(self, key: KeyType, default: T) -> Union[ValueType, T]: ...
    def add(self, key: KeyType, value: ValueType) -> None: ...
    def __getitem__(self, key: KeyType) -> ValueType: ...
    def __iter__(self) -> Iterator[KeyType]: ...
    def __len__(self) -> int: ...
