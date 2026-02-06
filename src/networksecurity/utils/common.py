from pathlib import Path
from typing import Any, Dict

import yaml

from networksecurity.exception import NetworkSecurityException


def read_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Read YAML file and return dict data."""
    try:
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)
            return content or {}
    except Exception as exc:
        raise NetworkSecurityException(str(exc)) from exc
