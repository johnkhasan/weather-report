"""Clean raw API data into a tidy table."""

import pandas as pd

# Short names are easier to read in the analysis and plotting code
COLUMN_NAMES = {
    "time": "date",
    "temperature_2m_mean": "temp_mean",
    "temperature_2m_max": "temp_max",
    "precipitation_sum": "precip",
}


def clean_weather(df, city):
    """Clean the raw daily weather of one city.

    Missing values are dropped, not interpolated. A check of all three
    cities for 1950–2025 found no missing values at all, so dropping is
    only a safety net. If a few days were ever missing, removing them
    barely changes yearly averages, while interpolation would invent
    values that were never measured.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw data as returned by ``load_city``.
    city : str
        City name, stored in a new ``city`` column.

    Returns
    -------
    pandas.DataFrame
        Columns: date, temp_mean, temp_max, precip, city.
    """
    cleaned = df.rename(columns=COLUMN_NAMES)
    cleaned["date"] = pd.to_datetime(cleaned["date"])
    cleaned["city"] = city

    missing = cleaned.isna().sum().sum()
    if missing > 0:
        print(f"{city}: dropping rows with {missing} missing values")
        cleaned = cleaned.dropna()

    return cleaned
