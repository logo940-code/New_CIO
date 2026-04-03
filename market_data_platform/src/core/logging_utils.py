import logging
import logging.config
from pathlib import Path
import yaml


def setup_logging(config_path: Path) -> None:
    with config_path.open('r', encoding='utf-8') as f:
        logging.config.dictConfig(yaml.safe_load(f))
