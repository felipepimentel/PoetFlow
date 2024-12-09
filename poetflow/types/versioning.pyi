"""Type stubs for versioning functionality."""
from dataclasses import dataclass
from typing import List, Optional

class SemanticVersionManager:
    """Manages semantic versioning"""
    def parse_commits(self, commits_data: str) -> List["CommitInfo"]: ...
    def determine_bump_type(self, commits: List["CommitInfo"]) -> str: ...
    def bump_version(self, current_version: str, bump_type: str) -> str: ...

@dataclass
class CommitInfo:
    """Information about a commit"""
    hash: str
    type: str
    scope: Optional[str]
    message: str
    breaking: bool 