"""Plotting functions. Each one returns a figure and never calls plt.show(),
so the same function works in Streamlit and in a notebook."""

import matplotlib.pyplot as plt
import seaborn as sns

WARM_COLOR = "#e34948"  # red: warmer than the baseline
COOL_COLOR = "#2a78d6"  # blue: colder than the baseline

# A fixed color per city, so a city looks the same in every chart
CITY_COLORS = {"Tashkent": "#eb6834", "Milan": "#1baf7a", "Oslo": "#6250d6"}


def plot_anomalies(yearly, city):
    """Bar chart of yearly temperature anomalies for one city.

    Parameters
    ----------
    yearly : pandas.DataFrame
        Output of ``add_anomalies``.
    city : str
        City to plot.

    Returns
    -------
    matplotlib.figure.Figure
    """
    data = yearly[yearly["city"] == city]
    fig, ax = plt.subplots(figsize=(10, 4))

    colors = [WARM_COLOR if value > 0 else COOL_COLOR for value in data["anomaly"]]
    ax.bar(data["year"], data["anomaly"], color=colors, width=0.8)
    ax.axhline(0, color="gray", linewidth=1)

    ax.set_title(f"{city}: yearly temperature anomaly vs 1961–1990")
    ax.set_xlabel("Year")
    ax.set_ylabel("Anomaly (°C)")
    # Only the zero line matters here, so remove the box around the plot
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    return fig


def plot_monthly_heatmap(monthly, city):
    """Heatmap of monthly mean temperature: months down, years across.

    Parameters
    ----------
    monthly : pandas.DataFrame
        Output of ``monthly_means``.
    city : str
        City to plot.

    Returns
    -------
    matplotlib.figure.Figure
    """
    data = monthly[monthly["city"] == city]
    table = data.pivot_table(index="month", columns="year", values="temp_mean")

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(table, cmap="YlOrRd", ax=ax, cbar_kws={"label": "Mean temperature (°C)"})

    ax.set_title(f"{city}: monthly mean temperature")
    ax.set_xlabel("Year")
    ax.set_ylabel("Month")
    fig.tight_layout()
    return fig


def plot_city_comparison(yearly):
    """Line chart of all cities' anomalies, smoothed with a 10-year mean.

    Parameters
    ----------
    yearly : pandas.DataFrame
        Output of ``add_anomalies``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 4))

    for city, data in yearly.groupby("city"):
        # Single years are noisy; a 10-year average shows the long-term shape
        smoothed = data["anomaly"].rolling(10).mean()
        color = CITY_COLORS.get(city, "gray")
        ax.plot(data["year"], smoothed, color=color, linewidth=2, label=city)
        # Name each line at its end, so it is readable without matching colors
        ax.text(data["year"].iloc[-1] + 1, smoothed.iloc[-1], city,
                color=color, va="center")

    ax.axhline(0, color="gray", linewidth=1)
    ax.set_title("Temperature anomaly vs 1961–1990 (10-year rolling mean)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Anomaly (°C)")
    ax.legend(loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    return fig


def plot_hot_days(hot_days):
    """Line chart of hot days per year for all cities, smoothed with a 10-year mean.

    Parameters
    ----------
    hot_days : pandas.DataFrame
        Output of ``hot_days_per_year``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 4))

    for city, data in hot_days.groupby("city"):
        smoothed = data["hot_days"].rolling(10).mean()
        color = CITY_COLORS.get(city, "gray")
        ax.plot(data["year"], smoothed, color=color, linewidth=2, label=city)
        ax.text(data["year"].iloc[-1] + 1, smoothed.iloc[-1], city,
                color=color, va="center")

    ax.set_title("Hot days per year (10-year rolling mean)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Days above the city's 95th percentile")
    ax.legend(loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    return fig
