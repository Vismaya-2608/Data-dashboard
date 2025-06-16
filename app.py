
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Additional Data Analysis", layout="wide")

st.sidebar.title("Additional_data")


# Read the Excel file
Preview,Alldata,Datasummary = st.tabs(["Preview","Quick Summary","Data Summary"])
with Preview:
  excel_file_path = 'All_DataFrames.xlsx'
  xls = pd.ExcelFile(excel_file_path)
  sheet_names = xls.sheet_names
  sheet = st.selectbox("Select Data file", sheet_names)

  # Read selected sheet
  df = pd.read_excel(excel_file_path, sheet_name=sheet)

  # Display DataFrame
  st.dataframe(df, use_container_width=True)
  
with Alldata:
  excel_file_path = "Quick_data_summary.xlsx"
  xls = pd.ExcelFile(excel_file_path)
  #sheet_names = xls.sheet_names
  #sheet = st.selectbox("Select sheet", sheet_names)

  # Read selected sheet
  df = pd.read_excel(excel_file_path, sheet_name=0)
  #st.success(f"Showing data from '{sheet}'")
 
  # Display DataFrame
  st.dataframe(df, use_container_width=True)
  
with Datasummary:
  excel_file_path = 'Data_Summaries.xlsx'
  xls = pd.ExcelFile(excel_file_path)
  sheet_names = xls.sheet_names
  sheet = st.selectbox("Select Data file", sheet_names)

  # Read selected sheet
  df = pd.read_excel(excel_file_path, sheet_name=sheet)

  # Display DataFrame
  st.dataframe(df, use_container_width=True)
