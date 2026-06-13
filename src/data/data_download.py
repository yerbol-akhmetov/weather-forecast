# SPDX-FileCopyrightText:  Weather-Forecast authors
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from utils.config import load_config
from utils.logging import setup_logger


def main() -> None:
    logger = setup_logger("data_download")

    config = load_config()
    config_data = config["data_download"]

    logger.info("Starting download for %s", config_data["name"])

    cache_session = requests_cache.CachedSession(
        config_data["cache_dir"],
        expire_after=config_data["cache_expire_after"],
    )
    retry_session = retry(
        cache_session,
        retries=config_data["retries"],
        backoff_factor=0.2,
    )
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = config_data["archive_url"]
    params = {
        "latitude": config_data["latitude"],
        "longitude": config_data["longitude"],
        "start_date": config_data["start_date"],
        "end_date": config_data["end_date"],
        "hourly": config_data["hourly_variables"],
        "wind_speed_unit": config_data["wind_speed_unit"],
        "timezone": config_data["timezone"],
    }
    logger.info(
        "Requesting data from %s to %s",
        config_data["start_date"],
        config_data["end_date"],
    )

    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    logger.info(
        "Coordinates: %s°N %s°E",
        response.Latitude(),
        response.Longitude(),
    )
    logger.info("Elevation: %s m asl", response.Elevation())
    logger.info("Timezone offset from GMT+0: %ss", response.UtcOffsetSeconds())

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(5).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["pressure_msl"] = hourly_pressure_msl

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    logger.info("Downloaded %s rows", len(hourly_dataframe))
    logger.info(
        "Date range: %s to %s",
        hourly_dataframe["date"].min(),
        hourly_dataframe["date"].max(),
    )
    logger.info("Preview:\n%s", hourly_dataframe.head())

    hourly_dataframe.to_csv(config_data["output_path"], index=False)
    logger.info("Saved to %s", config_data["output_path"])


if __name__ == "__main__":
    main()
