"""Type stubs for configuration."""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

@dataclass
class MonorangerConfig:
    """Configuration for Monoranger plugin"""
    enabled: bool
    monorepo_root: Path
    packages_dir: Optional[str] = None
    version_rewrite_rule: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "MonorangerConfig": ... 