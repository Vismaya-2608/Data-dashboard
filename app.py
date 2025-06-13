import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(layout="wide")
#st.markdown("Data Summary of New Files")
sidebar_option = st.sidebar.radio("Choose View", [
    "Data Summary",
    "Univariate analysis",
])
# --- View 1: Data Summary ---
if sidebar_option == "Data Summary":
    st.subheader("📄 Summary of all data")
    tab1, tab2 = st.tabs(["Preview", "Summary"])
    with tab1:
        sample = "All_DataFrames.xlsx"
        sample_df = pd.read_csv(sample)
        st.dataframe(sample_df)


