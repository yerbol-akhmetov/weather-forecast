# Weather Forecast

Machine learning project to forecast weather in Astana using historical data from [Open-Meteo](https://open-meteo.com/) and scikit-learn.

The workflow is:

1. Download hourly weather data for Astana
2. Preprocess and engineer features (planned)
3. Train and evaluate ML models (planned)

## Project structure

```
weather-forecast/
├── configs/           # Shared settings (location, dates, variables)
├── data/
│   ├── raw/           # Downloaded CSV files
│   └── processed/     # Cleaned data for modeling
├── logs/              # Log files per script
├── notebooks/         # Exploratory analysis
├── outputs/           # Models, plots, reports
├── src/
│   ├── data/          # Data download scripts
│   ├── models/        # Model definitions
│   └── training/      # Training scripts
└── utils/             # Config and logging helpers
```

## Environment setup

Requires **Python 3.11+**.

### 1. Clone the repository

```bash
git clone git@github.com:yerbol-akhmetov/weather-forecast.git
cd weather-forecast
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv .weather-env
.weather-env\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv .weather-env
source .weather-env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pre-commit install
```

`pre-commit install` sets up automatic lint checks before each commit. See [`docs/pre-commit.md`](docs/pre-commit.md) for details.

## Downloading data

All download settings live in [`configs/config.default.yaml`](configs/config.default.yaml) under the `data_download` section: location, date range, weather variables, and output path.

Run from the project root (`weather-forecast/`):

```bash
python -m src.data.data_download
```

Do not run from inside `src/data/` (for example `python data_download.py`) — imports like `from utils.config` will fail.

### Output

| Output | Location |
|---|---|
| CSV file | `data/raw/astana_hourly.csv` |
| Logs | `logs/data_download/` |
| API cache | `.cache/` (reused on later runs) |

### Configure the download

Edit `configs/config.default.yaml` to change, for example:

- `start_date` / `end_date` — time range
- `hourly_variables` — weather fields from Open-Meteo
- `latitude` / `longitude` — coordinates
- `output_path` — where to save the CSV
