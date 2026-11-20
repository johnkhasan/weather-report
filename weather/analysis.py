"""Aggregations and climate statistics."""

import numpy as np
import pandas as pd
from scipy import stats

from weather.config import BASELINE_YEARS


def add_date_parts(df):
    """Return a copy of ``df`` with ``year`` and ``month`` columns added.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily data with a datetime ``date`` column.

    Returns
    -------
    pandas.DataFrame
        The same data plus integer ``year`` and ``month`` columns.
    """
    # assign() returns a new table, so the caller's data is not modified
    return df.assign(year=df["date"].dt.year, month=df["date"].dt.month)


def yearly_means(df):
    """Average daily mean temperature per city and year.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily data from ``build_dataset``.

    Returns
    -------
    pandas.DataFrame
        Columns: city, year, temp_mean.
    """
    daily = add_date_parts(df)
    return daily.groupby(["city", "year"])["temp_mean"].mean().reset_index()


def monthly_means(df):
    """Average daily mean temperature per city, year and month.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily data from ``build_dataset``.

    Returns
    -------
    pandas.DataFrame
        Columns: city, year, month, temp_mean.
    """
    daily = add_date_parts(df)
    return daily.groupby(["city", "year", "month"])["temp_mean"].mean().reset_index()


def add_anomalies(yearly):
    """Add each year's difference from the city's 1961–1990 average.

    Parameters
    ----------
    yearly : pandas.DataFrame
        Output of ``yearly_means``.

    Returns
    -------
    pandas.DataFrame
        The same table plus ``baseline`` and ``anomaly`` columns (°C).
    """
    start, end = BASELINE_YEARS
    in_baseline = yearly["year"].between(start, end)
    baseline = yearly[in_baseline].groupby("city")["temp_mean"].mean()

    # map() looks up each row's city in the baseline Series
    with_baseline = yearly.assign(baseline=yearly["city"].map(baseline))
    with_baseline["anomaly"] = with_baseline["temp_mean"] - with_baseline["baseline"]
    return with_baseline


def warming_trend(yearly):
    """Fit a straight line through yearly temperatures for each city.

    Parameters
    ----------
    yearly : pandas.DataFrame
        Output of ``yearly_means`` (or ``add_anomalies``).

    Returns
    -------
    pandas.DataFrame
        One row per city. Columns: city, trend_per_decade (°C per
        10 years) and p_value.
    """
    rows = []
    for city, data in yearly.groupby("city"):
        result = stats.linregress(data["year"], data["temp_mean"])
        rows.append({
            "city": city,
            # slope is °C per year; per decade is easier to read
            "trend_per_decade": result.slope * 10,
            "p_value": result.pvalue,
        })
    return pd.DataFrame(rows)


def hot_day_thresholds(df):
    """Find each city's hot-day limit: the 95th percentile of baseline temp_max.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily data from ``build_dataset``.

    Returns
    -------
    pandas.Series
        Threshold in °C, indexed by city.
    """
    start, end = BASELINE_YEARS
    baseline_days = df[df["date"].dt.year.between(start, end)]

    thresholds = {}
    for city, data in baseline_days.groupby("city"):
        thresholds[city] = np.percentile(data["temp_max"], 95)
    return pd.Series(thresholds)


def hot_days_per_year(df):
    """Count days per year hotter than the city's own baseline threshold.

    A day is "hot" when its temp_max is above the 95th percentile of
    1961–1990 for that city, so each city is judged by its own climate.

    Parameters
    ----------
    df : pandas.DataFrame
        Daily data from ``build_dataset``.

    Returns
    -------
    pandas.DataFrame
        Columns: city, year, hot_days.
    """
    daily = add_date_parts(df)
    threshold = daily["city"].map(hot_day_thresholds(df))
    daily["is_hot"] = daily["temp_max"] > threshold

    # Summing True/False counts the True values, and years with no hot
    # days still appear with 0
    hot_days = daily.groupby(["city", "year"])["is_hot"].sum()
    return hot_days.reset_index(name="hot_days")
