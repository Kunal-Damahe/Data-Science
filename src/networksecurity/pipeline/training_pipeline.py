from networksecurity.config.configuration import ConfigurationManager
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logger


class TrainingPipeline:
    """Phase-wise orchestration class.

    Phase 0: setup and config loading only.
    """

    def __init__(self) -> None:
        self.config = ConfigurationManager()

    def run_pipeline(self) -> None:
        try:
            train_config = self.config.get_training_pipeline_config()
            data_ingestion_config = self.config.get_data_ingestion_config()

            logger.info("Pipeline name: %s", train_config.pipeline_name)
            logger.info("Artifact dir: %s", train_config.artifact_dir)
            logger.info(
                "Data ingestion source: %s.%s",
                data_ingestion_config.database_name,
                data_ingestion_config.collection_name,
            )
            logger.info("Phase 0 setup completed successfully.")
        except Exception as exc:
            raise NetworkSecurityException(str(exc)) from exc
