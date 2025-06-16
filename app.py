
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Additional Data Analysis", layout="wide")

st.sidebar.title("Additional_data")


# Read the Excel file
Preview, Alldata, Datasummary, Charts = st.tabs(["Preview", "Quick Summary", "Data Summary", "Charts"])

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

with Charts:
    st.title("Time Series Chart from Local Excel File")

    # Step 1: Read Excel file from disk
    excel_file_path = "Dsc_Average_Construction_Materi.xlsx"  # Change this to your actual file path
    df = pd.read_excel(excel_file_path)

    # Step 2: Show data preview
    st.write("Data Preview:")
    st.dataframe(df)

    # Step 3: Detect 'Year' column
    year_columns = [col for col in df.columns if 'year' in col.lower()]
    if year_columns:
        year_col = year_columns[0]
    else:
        st.error("No column with name containing 'year' found.")
        st.stop()

    # Step 4: Select Y-axis column
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    y_col = st.selectbox("Select column for Y-axis", options=[col for col in numeric_columns if col != year_col])

    # Step 5: Plot the time series chart
    if y_col:
        fig, ax = plt.subplots()
        ax.plot(df[year_col], df[y_col], marker='o')
        ax.set_xlabel(year_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"Time Series: {y_col} over {year_col}")
        ax.grid(True)
        st.pyplot(fig)
