from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionArtifact:
    feature_store_file_path: Path
    used_fallback: bool
    message: str
