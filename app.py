"""Streamlit app: only calls functions from the weather package, no calculations here."""

import streamlit as st

from weather import analysis, plots
from weather.clean import build_dataset

st.set_page_config(page_title="Weather Report", layout="wide")


@st.cache_data
def get_data():
    """Load the combined dataset once; Streamlit reuses it on every rerun."""
    return build_dataset()


df = get_data()
yearly = analysis.add_anomalies(analysis.yearly_means(df))
monthly = analysis.monthly_means(df)
trends = analysis.warming_trend(yearly).set_index("city")
hot_days = analysis.hot_days_per_year(df)
thresholds = analysis.hot_day_thresholds(df)

st.title("Weather Report")
st.write("How has the climate changed in Tashkent, Milan and Oslo since 1950?")
st.caption("Data: Open-Meteo historical archive, daily values 1950–2025.")

city = st.sidebar.selectbox("City", sorted(df["city"].unique()))

overview_tab, city_tab, extremes_tab = st.tabs(["Overview", "City detail", "Extremes"])

with overview_tab:
    columns = st.columns(len(trends))
    for column, (name, row) in zip(columns, trends.iterrows()):
        column.metric(f"{name} warming trend", f"{row['trend_per_decade']:+.2f} °C/decade")

    st.pyplot(plots.plot_city_comparison(yearly))
    st.write(
        "All three cities are now warmer than in 1961–1990. Milan and Oslo "
        "started warming around 1990, while Tashkent stayed close to normal "
        "until about 2000 and has warmed quickly since then."
    )

with city_tab:
    trend = trends.loc[city]
    st.metric(
        f"{city} warming trend 1950–2025",
        f"{trend['trend_per_decade']:+.2f} °C/decade",
    )
    st.caption(f"p-value = {trend['p_value']:.1e}: the trend is very unlikely to be random.")

    st.pyplot(plots.plot_anomalies(yearly, city))
    st.write(
        "Red bars are years warmer than the 1961–1990 average, blue bars are "
        "colder. Before 1990 both colors are mixed; in the last two decades "
        "almost every year is red."
    )

    st.pyplot(plots.plot_monthly_heatmap(monthly, city))
    st.write(
        "The seasons dominate this chart, but the winter rows get warmer "
        "colors in recent years, so winters are warming too, not only summers."
    )

with extremes_tab:
    st.write(
        "A day counts as hot when its maximum temperature is above the city's "
        "own 95th percentile for 1961–1990: "
        + ", ".join(f"{name} {limit:.1f} °C" for name, limit in thresholds.items())
        + "."
    )
    st.pyplot(plots.plot_hot_days(hot_days))
    st.write(
        "In 1961–1990 each city had about 18 hot days a year. In 2016–2025 "
        "Milan had about 56, Tashkent about 41 and Oslo about 27."
    )
