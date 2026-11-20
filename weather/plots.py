"""Plotting functions. Each one returns a figure and never calls plt.show(),
so the same function works in Streamlit and in a notebook."""

import matplotlib.pyplot as plt

WARM_COLOR = "#e34948"  # red: warmer than the baseline
COOL_COLOR = "#2a78d6"  # blue: colder than the baseline


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
