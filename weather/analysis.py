"""Aggregations and climate statistics."""


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
