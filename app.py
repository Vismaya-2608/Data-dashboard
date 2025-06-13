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
        excel_file = "All_DataFrames.xlsx"
        all_sheets = pd.read_excel(excel_file, sheet_name=None)  # Returns a dict of {sheet_name: dataframe}
        # Get list of sheet names for dropdown
sheet_names = list(all_sheets.keys())
# Dropdown to select sheet (cat_col)
selected_sheet = st.selectbox("Select a sheet to display:", sheet_names)
# Display the selected sheet as dataframe
if selected_sheet:
    df = all_sheets[selected_sheet]
    st.write(f"### Data from Sheet: {selected_sheet}")
    st.dataframe(df)

