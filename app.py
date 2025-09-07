import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Additional Data Analysis", layout="wide")
st.sidebar.title("DUBAI Econometrics")

# Sidebar main tab selection
main_tab = st.sidebar.radio("View", ["Data Inventory", "Data Summary", "Data Explorer", "Merged Dataset"])

# Excel paths outside
excel_file_path = 'All_DataFrames_final.xlsx'
excel_file_path1 = 'All_DataFrames_final_oilGold_removed.xlsx'
q_summary_path = "Quick_data_summary_final.xlsx"
summary_path = 'Data_Summaries_final.xlsx'
summary = "macro_dataset_summary_combined_above_2020.xlsx"

# Load sheet names once
xls_main = pd.ExcelFile(excel_file_path)
sheet_names_main = xls_main.sheet_names



# ============== DATA SECTION =================
if main_tab == "Data Inventory":
        df = pd.read_excel(q_summary_path, sheet_name=0)
        #st.subheader("⚡ Quick Summary")
        st.dataframe(df, use_container_width=True)
        
# ============== DATA SECTION =================
elif main_tab == "Data Summary":
    xls_summary = pd.ExcelFile(summary_path)
    sheet_names_summary = xls_summary.sheet_names
    
    sheet = st.selectbox("Select Data Frame", sheet_names_summary, key="chart_sheet")
    tab1,tab2 = st.tabs(["Summary","Notes"])
        
    with tab1:
        xls_summary = pd.ExcelFile(summary_path)
        sheet_names_summary = xls_summary.sheet_names
        if sheet in sheet_names_summary:
            df1 = pd.read_excel(summary_path, sheet_name=sheet)
            # st.subheader(f"📄 Data Summary: {sheet}")
            st.dataframe(df1, use_container_width=True)

    with tab2:
        st.markdown(
        """
        - Macro Datasets considered for merging:  
           - GDP quarterly  
           - Producer Price Index  
           - Consumer Price Index  
           - Consumer Cost Index  
           - Gold Price  
           - Oil Price  
        - Performed **groupby** based on `year`  
        - Considered dataset for **year > 2020** for merging with main data  
        """
        )

# ============== CHARTS SECTION =================

elif main_tab == "Data Explorer":
    # Check if file exists before trying to load
    if os.path.exists(excel_file_path1):
        xls_main1 = pd.ExcelFile(excel_file_path1)
        sheet_names_main1 = xls_main1.sheet_names
    else:
        st.error(f"❌ File not found: {excel_file_path1}")
        sheet_names_main1 = []

    main_tabs = st.tabs(["Table","Charts"])

    with main_tabs[0]:
        sheet = st.selectbox("Select Data Frame", sheet_names_main, key="chart_sheet_table")
        df2 = pd.read_excel(excel_file_path, sheet_name=sheet)
        st.dataframe(df2, use_container_width=True)

  with main_tabs[1]:
      if sheet_names_main1:
          # Create both tabs
          Dimensions_tab, Metics_tab = st.tabs(["Dimensions","Metrics"])

          # ================= Dimensions Tab =================
          with Dimensions_tab:
              # 👇 Move the sheet selector here (only for Dimensions)
              sheet = st.selectbox("Select Data Frame", sheet_names_main1, key="chart_sheet_chart")

              df = pd.read_excel(excel_file_path, sheet_name=sheet)
              categorical_columns = df.select_dtypes(include=['object', 'string']).columns.tolist()
              numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

              show_legend = st.checkbox("Show Legend", value=True)

              if "year" not in df.columns:
                  st.error("❌ 'year' column not found in the dataset.")
              else:
                  plot_type = st.sidebar.selectbox("Select Plot Type", ["Time Series", "Distribution"], key="plot_type")
                  id_cols = ['id', 'i_d', 'year', 'quantityar', 'quantityen']

                  if plot_type == "Time Series":
                      category_col = st.sidebar.selectbox("Select Dimensions (Legend)", categorical_columns, key="line_legend")
                      value_col = st.sidebar.selectbox("Select Metrics (Y-Axis)", [col for col in numeric_columns if col not in id_cols], key="line_y")

                      df_grouped = df.groupby(['year', category_col])[value_col].mean().reset_index()

                      fig = px.line(
                          df_grouped.dropna(subset=["year", value_col, category_col]),
                          x="year",
                          y=value_col,
                          color=category_col,
                          markers=True,
                          title=f"{value_col} over Years by {category_col}"
                      )
                  else:
                      df["year"] = df["year"].astype(str)
                      category_col = st.sidebar.selectbox("Select Dimension (X-Axis)", categorical_columns, key="bar_x")
                      value_col = st.sidebar.selectbox("Select Metrics (Y-Axis)", [col for col in numeric_columns if col not in id_cols], key="bar_y")

                      total_df = df.groupby(category_col)[value_col].sum().reset_index()
                      total_df.rename(columns={value_col: "total_value"}, inplace=True)
                      df = df.merge(total_df, on=category_col, how='left')

                      fig = px.bar(
                          df.dropna(subset=["year", value_col, category_col]),
                          x=category_col,
                          y=value_col,
                          title=f"{value_col} by {category_col}",
                          hover_name=category_col,
                          hover_data={"total_value": True, value_col: True, "year": True}
                      )

                  fig.update_layout(
                      xaxis=dict(tickangle=45),
                      showlegend=show_legend,
                      legend=dict(orientation="v", yanchor="top", y=1.1, xanchor="left", x=1.02)
                  )
                  st.plotly_chart(fig, use_container_width=True)

          # ================= Metrics Tab =================
          with Metics_tab:
              metrics_file_path = "Only Gold and oil.xlsx"
              if os.path.exists(metrics_file_path):
                  sheet_names_metrics = pd.ExcelFile(metrics_file_path).sheet_names
                  sheet_metrics = st.selectbox("Select Metrics Data Frame", sheet_names_metrics, key="metrics_sheet")
                  df_metrics = pd.read_excel(metrics_file_path, sheet_name=sheet_metrics)

                  numeric_columns = df_metrics.select_dtypes(include=['number']).columns.tolist()

                  if "year" not in df_metrics.columns:
                      st.error("❌ 'year' column not found in the metrics dataset.")
                  else:
                      value_col = st.selectbox("Select Metric (Y-Axis)", numeric_columns, key="metrics_y")

                      df_grouped = df_metrics.groupby("year", as_index=False)[value_col].mean()

                      fig = px.line(
                          df_grouped.dropna(subset=["year", value_col]),
                          x="year",
                          y=value_col,
                          markers=True,
                          title=f"{value_col} over Years"
                      )
                      fig.update_layout(showlegend=False)
                      st.plotly_chart(fig, use_container_width=True)
              else:
                  st.error(f"❌ Metrics file not found: {metrics_file_path}")

      else:
          st.warning("⚠️ Charts not available because the Excel file is missing.")


                
         
# ============== DATA SECTION =================
elif main_tab == "Merged Dataset":
    tab1, = st.tabs(["Summary"])  # removed extra comma
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Number Of Columns", value=55)

        with col2:
            st.metric(label="Total Records", value="588,863")

        with col3:
            st.metric(label="Start Date (Instance_Date)", value="2020-01-02")

        with col4:
            st.metric(label="End Date (Instance_Date)", value="2025-04-03")
                
        summary_df = pd.read_excel(summary)
        # Format all numeric columns with commas
        for col in summary_df.select_dtypes(include='number').columns:
            summary_df[col] = summary_df[col].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else x)
    
        summary_df.index = range(1, len(summary_df) + 1)
        #summary_df.rename(columns={'No_of_units': 'Num_of_Unique_values'}, inplace=True)
        #summary_df = summary_df.drop(columns = ["S.no", "Level"])
        st.dataframe(summary_df)

        
        
        
                

