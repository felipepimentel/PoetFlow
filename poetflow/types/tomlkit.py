"""Type definitions for tomlkit interactions"""

from tomlkit import TOMLDocument as _TOMLDocument
from tomlkit import api as _api
from tomlkit import parse as _parse

TOMLDocument = _TOMLDocument
api = _api
parse = _parse

__all__ = ["TOMLDocument", "api", "parse"] 