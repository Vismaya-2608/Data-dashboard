import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Additional Data Analysis", layout="wide")
st.sidebar.title("📊 Additional Data Explorer")

# Sidebar main tab selection
main_tab = st.sidebar.radio("Select View", ["Data", "📈 Chart Visualization"])

# Excel paths outside
excel_file_path = 'All_DataFrames.xlsx'
q_summary_path = "Quick_data_summary.xlsx"
summary_path = 'Data_Summaries.xlsx'

# Load sheet names once
xls_main = pd.ExcelFile(excel_file_path)
sheet_names_main = xls_main.sheet_names

# ============== DATA SECTION =================
if main_tab == "Data":
    tab1, tab2, tab3 = st.tabs(["🔍Preview", "⚡Quick Summary", "📄 Data Summary"])

    with tab1:
        sheet = st.selectbox("Select Data file", sheet_names_main, key="preview_data")
        df = pd.read_excel(excel_file_path, sheet_name=sheet)
        #st.subheader(f"🔍 Preview: {sheet}")
        st.dataframe(df, use_container_width=True)

    with tab2:
        df = pd.read_excel(q_summary_path, sheet_name=0)
        #st.subheader("⚡ Quick Summary")
        st.dataframe(df, use_container_width=True)

    with tab3:
        xls_summary = pd.ExcelFile(summary_path)
        sheet_names_summary = xls_summary.sheet_names
        sheet = st.selectbox("Select Summary file", sheet_names_summary, key="summary_data")
        df = pd.read_excel(summary_path, sheet_name=sheet)
        #st.subheader(f"📄 Data Summary: {sheet}")
        st.dataframe(df, use_container_width=True)

# ============== CHARTS SECTION =================
elif main_tab == "📈 Chart Visualization":
    sheet = st.selectbox("Select Data file", sheet_names_main, key="chart_sheet")
    df = pd.read_excel(excel_file_path, sheet_name=sheet)

    # Identify column types
    categorical_columns = df.select_dtypes(include=['object', 'string']).columns.tolist()
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    # Chart type selector in sidebar
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Line", "Bar"], key="plot_type")

    # Ensure 'year' column is present
    if "year" not in df.columns:
        st.error("❌ 'year' column not found in the dataset.")
    else:
        id_cols = ['id', 'i_d', 'year','quantityar','quantityen']

        if plot_type == "Line":
            value_col = st.sidebar.selectbox(
                "Select Numeric Column (Y-Axis)",
                [col for col in numeric_columns if col not in id_cols],
                key="line_y"
            )
            category_col = st.sidebar.selectbox(
                "Select Category Column (Legend)",
                categorical_columns,
                key="line_legend"
            )

            # Aggregate the data
            df_grouped = df.groupby(['year', category_col])[value_col].mean().reset_index()

            fig = px.line(
                df_grouped.dropna(subset=["year", value_col, category_col]),
                x="year",
                y=value_col,
                color=category_col,
                markers=True,
                title=f"{value_col} over Years by {category_col}"
            )

        else:  # Bar chart
            df["year"] = df["year"].astype(str)

            category_col = st.sidebar.selectbox(
                "Select Category Column (X-Axis)",
                categorical_columns,
                key="bar_x"
            )
            
            value_col = st.sidebar.selectbox(
                "Select Numeric Column (Y-Axis)",
                [col for col in numeric_columns if col not in id_cols],
                key="bar_y"
            )

            fig = px.bar(
                df.dropna(subset=["year", value_col, category_col]),
                x=category_col,
                y=value_col,
                title=f"{value_col} by {category_col}"
            )
            fig.update_layout(barmode='overlay')  # Show bars overlaid (not stacked)

        st.plotly_chart(fig, use_container_width=True)
