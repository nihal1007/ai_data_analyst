import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

from services.data_loader import load_dataset
from services.eda_engine import run_eda
from services.insights_engine import generate_insights
from components.sidebar import display_sidebar

from services.data_cleaning import (
    remove_duplicate_rows,
    handle_missing_values,
    get_cleaning_summary,
)
from components.dashboard import (
    display_overview,
    display_missing_values,
    display_numeric_summary,
    display_insights,
    display_visualizations,
)
from services.statistical_analysis import (
    get_statistical_summary,
    get_correlation_matrix,
)
from components.charts import (
    create_histogram,
    create_box_plot,
    create_correlation_heatmap,
)

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="DataMind AI | Data Analyst",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# CUSTOM STYLING
# -------------------------------

st.markdown("""
<style>
    .main {
        background-color: #0b1120;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3 {
        color: #e2e8f0;
    }

    .metric-card {
        background-color: #151f32;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #273449;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------

st.title("📊 DataMind AI")
st.caption(
    "Automated Exploratory Data Analysis · "
    "Statistical Insights · Interactive Visualizations"
)

st.divider()

# -------------------------------
# FILE UPLOAD
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info(
        "Upload a CSV or Excel file to generate "
        "an automatic data analysis report."
    )

    st.subheader("What you will get")
    col1, col2, col3 = st.columns(3)

    col1.markdown("### 🔎 Dataset Overview")
    col1.write("Rows, columns, data types, and missing values.")

    col2.markdown("### 📈 Interactive Charts")
    col2.write("Histograms, scatter plots, and correlation heatmaps.")

    col3.markdown("### 💡 Data Insights")
    col3.write("Statistical findings and data-quality observations.")

    st.stop()

# -------------------------------
# READ DATASET
# -------------------------------

try:
    df = load_dataset(uploaded_file)

except ValueError as error:
    st.error(str(error))
    st.stop()

# -------------------------------
# SIDEBAR OPTIONS
# -------------------------------

sidebar_options = display_sidebar()

# Keep a copy of the original dataset for comparison
original_df = df.copy()

# -------------------------------
# DATA CLEANING
# -------------------------------

missing_strategy = sidebar_options["missing_strategy"]

if missing_strategy != "None":
    strategy_map = {
        "Drop Rows": "drop",
        "Mean": "mean",
        "Median": "median",
        "Mode": "mode",
    }

    df = handle_missing_values(
        df,
        strategy=strategy_map[missing_strategy]
    )

if sidebar_options["remove_duplicates"]:
    df = remove_duplicate_rows(df)

cleaning_summary = get_cleaning_summary(original_df, df)

# -------------------------------
# RUN EXPLORATORY DATA ANALYSIS
# -------------------------------

eda_results = run_eda(df)
statistical_summary = get_statistical_summary(df)
correlation_matrix = get_correlation_matrix(df)
insights = generate_insights(df)

# -------------------------------
# DATASET OVERVIEW
# -------------------------------

display_overview(eda_results["overview"])

# -------------------------------
# DATA PREVIEW
# -------------------------------

st.subheader("Dataset Preview")

st.dataframe(df.head(100), width="stretch")

# -------------------------------
# DATA TYPES
# -------------------------------

with st.expander("View column data types"):
    dtypes_df = pd.DataFrame({
        "Column": df.columns.astype(str),
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isna().sum().values,
        "Missing Percentage": (
            df.isna().mean().mul(100).round(2).values
        ),
        "Unique Values": df.nunique(dropna=True).values
    })

    st.dataframe(dtypes_df, width="stretch")

# -------------------------------
# STATISTICAL SUMMARY
# -------------------------------
numeric_df = df.select_dtypes(include="number")
display_numeric_summary(statistical_summary)

# -------------------------------
# MISSING VALUE ANALYSIS
# -------------------------------

display_missing_values(eda_results["missing_values"])

# -------------------------------
# NUMERICAL DISTRIBUTIONS
# -------------------------------

st.header("Numerical Data Visualization")

numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

if numeric_columns:
    selected_column = st.selectbox(
        "Choose a numerical column",
        numeric_columns
    )

    try:
        col1, col2 = st.columns(2)

        with col1:
            fig_hist = create_histogram(
                df,
                selected_column
            )

            st.plotly_chart(
                fig_hist,
                width="stretch"
            )

        with col2:
            fig_box = create_box_plot(
                df,
                selected_column
            )

            st.plotly_chart(
                fig_box,
                width="stretch"
            )

    except ValueError as error:
        st.warning(str(error))

else:
    st.info(
        "No numerical columns are available for visualization."
    )
# -------------------------------
# CORRELATION ANALYSIS
# -------------------------------

st.header("Correlation Analysis")

fig_corr = create_correlation_heatmap(df)

if fig_corr is not None:
    st.plotly_chart(
        fig_corr,
        width="stretch"
    )
else:
    st.info(
        "At least two numerical columns are required "
        "for correlation analysis."
    )
# -------------------------------
# AUTOMATIC INSIGHTS
# -------------------------------

display_insights(insights)

# -------------------------------
# DOWNLOAD ANALYSIS
# -------------------------------
missing_total = int(df.isna().sum().sum())
duplicate_total = int(df.duplicated().sum())
st.header("Download Analysis")

report = io.StringIO()

report.write("DATAMIND AI - DATA ANALYSIS REPORT\n\n")
report.write(f"Rows: {df.shape[0]}\n")
report.write(f"Columns: {df.shape[1]}\n")
report.write(f"Missing cells: {missing_total}\n")
report.write(f"Duplicate rows: {duplicate_total}\n\n")
report.write("STATISTICAL SUMMARY\n")

if not numeric_df.empty:
    report.write(numeric_df.describe().to_string())

st.download_button(
    label="Download Statistical Report (TXT)",
    data=report.getvalue(),
    file_name="datamind_analysis.txt",
    mime="text/plain"
)

st.divider()
st.caption(
    "DataMind AI · Automated analysis for better decisions"
)
