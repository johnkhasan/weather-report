"""Download historical daily weather from the Open-Meteo archive API."""

import requests

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
DAILY_VARIABLES = ["temperature_2m_mean", "temperature_2m_max", "precipitation_sum"]


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
    # TODO: send a GET request with a timeout (e.g. 60 seconds)
    # TODO: call raise_for_status() so HTTP errors are not silently ignored
    # TODO: wrap it in try/except requests.RequestException with a clear message
