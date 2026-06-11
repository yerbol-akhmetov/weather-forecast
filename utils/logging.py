# SPDX-FileCopyrightText:  Weather-Forecast authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"


def setup_logger(name: str, log_file: str | None = None) -> logging.Logger:
    log_dir = LOGS_DIR / name
    log_dir.mkdir(parents=True, exist_ok=True)

    if log_file is None:
        log_file = f"{datetime.now():%Y%m%d_%H%M%S}.log"

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_dir / log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
