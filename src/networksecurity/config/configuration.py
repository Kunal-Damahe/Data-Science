from pathlib import Path

from networksecurity.constants import CONFIG_FILE_PATH
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.utils.common import read_yaml_file


class ConfigurationManager:
    """Load and map YAML settings to typed config entities."""

    def __init__(self, config_file_path: Path = CONFIG_FILE_PATH) -> None:
        self.config_info = read_yaml_file(config_file_path)
        logger.info("Configuration loaded from %s", config_file_path)

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            pipeline_config = self.config_info["training_pipeline_config"]
            return TrainingPipelineConfig(
                pipeline_name=pipeline_config["pipeline_name"],
                artifact_dir=Path(pipeline_config["artifact_dir"]),
            )
        except KeyError as exc:
            raise NetworkSecurityException(
                f"Missing key in training_pipeline_config: {exc}"
            ) from exc

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            ingestion_config = self.config_info["data_ingestion_config"]
            return DataIngestionConfig(
                database_name=ingestion_config["database_name"],
                collection_name=ingestion_config["collection_name"],
                data_file_path=Path(ingestion_config["data_file_path"]),
                fallback_csv_path=Path(ingestion_config["fallback_csv_path"]),
            )
        except KeyError as exc:
            raise NetworkSecurityException(
                f"Missing key in data_ingestion_config: {exc}"
            ) from exc
