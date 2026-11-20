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

st.title("Weather Report")
st.write("How has the climate changed in Tashkent, Milan and Oslo since 1950?")

city = st.sidebar.selectbox("City", sorted(df["city"].unique()))

st.pyplot(plots.plot_anomalies(yearly, city))
