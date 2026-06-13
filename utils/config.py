# SPDX-FileCopyrightText:  Weather-Forecast authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path

import yaml


def load_config(path: Path | None = None) -> dict:
    if path is None:
        path = Path(__file__).resolve().parents[1] / "configs" / "config.default.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)
