
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
    st.title("Categorical Distribution Over Years")

    # Step 1: Read Excel file from disk
    excel_file_path = "Dsc_Average_Construction_Materi.xlsx"  # Adjust the path as needed
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

    # Step 4: Detect categorical columns
    cat_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if not cat_columns:
        st.error("No categorical columns found in the dataset.")
        st.stop()

    # Step 5: Select a categorical column for analysis
    selected_cat_col = st.selectbox("Select categorical column for Y-axis (distribution)", options=cat_columns)

    # Step 6: Group and count occurrences
    group_df = df.groupby([year_col, selected_cat_col]).size().reset_index(name='Count')

    # Step 7: Pivot the table for plotting
    pivot_df = group_df.pivot(index=year_col, columns=selected_cat_col, values='Count').fillna(0)

    # Step 8: Plot stacked bar chart
    st.subheader(f"Distribution of '{selected_cat_col}' Over Years")
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_df.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel(year_col)
    ax.set_ylabel("Count")
    ax.set_title(f"Distribution of {selected_cat_col} by {year_col}")
    ax.legend(title=selected_cat_col, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    st.pyplot(fig)
