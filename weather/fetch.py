"""Download historical daily weather from the Open-Meteo archive API."""

import time
from pathlib import Path

import pandas as pd
import requests

from weather.config import CITIES, END_DATE, START_DATE

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
DAILY_VARIABLES = ["temperature_2m_mean", "temperature_2m_max", "precipitation_sum"]

# Built from this file's location so it works no matter where the app is started
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"


def fetch_daily_weather(latitude, longitude, start_date, end_date):
    """Download daily weather for one location.

    Parameters
    ----------
    latitude, longitude : float
        Coordinates of the location.
    start_date, end_date : str
        Dates in YYYY-MM-DD format.

    Returns
    -------
    dict
        Parsed JSON response from the API.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": "auto",
    }
    try:
        # Without a timeout the program could wait forever if the server hangs
        response = requests.get(ARCHIVE_URL, params=params, timeout=60)
        if response.status_code == 429:
            # Open-Meteo limits requests per minute; wait for the limit to reset
            print("API rate limit reached, waiting 60 seconds...")
            time.sleep(60)
            response = requests.get(ARCHIVE_URL, params=params, timeout=60)
        # Turn HTTP errors (4xx/5xx) into exceptions instead of ignoring them
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Could not download weather data: {error}") from error

    return response.json()


def load_city(name):
    """Load daily weather for one city, downloading it only the first time.

    The raw API response is saved to ``data/raw/<name>.csv``. Later calls
    read that file instead of calling the API again.

    Parameters
    ----------
    name : str
        City name, must be a key in ``CITIES``.

    Returns
    -------
    pandas.DataFrame
        One row per day with the columns returned by the API.
    """
    path = RAW_DATA_DIR / f"{name}.csv"

    if path.exists():
        return pd.read_csv(path)

    latitude, longitude = CITIES[name]
    result = fetch_daily_weather(latitude, longitude, START_DATE, END_DATE)
    df = pd.DataFrame(result["daily"])

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df
