import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.pipeline.training_pipeline import TrainingPipeline


def main() -> None:
    try:
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
    except Exception as exc:
        logger.error("Pipeline execution failed: %s", exc)
        raise NetworkSecurityException(str(exc), sys) from exc


if __name__ == "__main__":
    main()
