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
    try:
        # Without a timeout the program could wait forever if the server hangs
        response = requests.get(ARCHIVE_URL, params=params, timeout=60)
        # Turn HTTP errors (4xx/5xx) into exceptions instead of ignoring them
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Could not download weather data: {error}") from error

    return response.json()
