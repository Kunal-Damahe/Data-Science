from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrainingPipelineConfig:
    pipeline_name: str
    artifact_dir: Path


@dataclass(frozen=True)
class DataIngestionConfig:
    database_name: str
    collection_name: str
    data_file_path: Path
    fallback_csv_path: Path
