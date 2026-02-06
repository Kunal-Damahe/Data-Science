from pathlib import Path

# Root paths
ROOT_DIR = Path(__file__).resolve().parents[3]
CONFIG_DIR = ROOT_DIR / "config"
LOG_DIR = ROOT_DIR / "logs"
ARTIFACT_DIR = ROOT_DIR / "artifacts"

# Config file
CONFIG_FILE_PATH = CONFIG_DIR / "config.yaml"

# Logging
LOG_FILE_NAME = "network_security.log"
LOG_FILE_PATH = LOG_DIR / LOG_FILE_NAME

# Pipeline defaults
TRAINING_PIPELINE_NAME = "network_security"
ARTIFACT_ROOT_DIR = "artifacts"
