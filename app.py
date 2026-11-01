import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

from services.data_loader import load_dataset

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
# DATASET OVERVIEW
# -------------------------------

st.header("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rows", f"{df.shape[0]:,}")
col2.metric("Total Columns", f"{df.shape[1]:,}")
col3.metric("Missing Cells", f"{int(df.isna().sum().sum()):,}")
col4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

# -------------------------------
# DATA PREVIEW
# -------------------------------

st.subheader("Dataset Preview")

st.dataframe(df.head(100), use_container_width=True)

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

    st.dataframe(dtypes_df, use_container_width=True)

# -------------------------------
# STATISTICAL SUMMARY
# -------------------------------

st.header("Statistical Summary")

numeric_df = df.select_dtypes(include=np.number)

if not numeric_df.empty:
    st.dataframe(
        numeric_df.describe().T.round(2),
        use_container_width=True
    )
else:
    st.info("No numerical columns were detected.")

# -------------------------------
# MISSING VALUE ANALYSIS
# -------------------------------

st.header("Missing Value Analysis")

missing_df = pd.DataFrame({
    "Column": df.columns.astype(str),
    "Missing Values": df.isna().sum().values,
    "Missing Percentage": (
        df.isna().mean().mul(100).round(2).values
    )
})

missing_df = missing_df[
    missing_df["Missing Values"] > 0
]

if not missing_df.empty:
    st.dataframe(missing_df, use_container_width=True)

    fig_missing = px.bar(
        missing_df,
        x="Column",
        y="Missing Values",
        title="Missing Values by Column"
    )

    st.plotly_chart(fig_missing, use_container_width=True)
else:
    st.success("No missing values were detected.")

# -------------------------------
# NUMERICAL DISTRIBUTIONS
# -------------------------------

st.header("Numerical Data Visualization")

if not numeric_df.empty:
    selected_column = st.selectbox(
        "Choose a numerical column",
        numeric_df.columns.tolist()
    )

    valid_values = numeric_df[selected_column].dropna()

    if not valid_values.empty:
        fig_hist = px.histogram(
            x=valid_values,
            nbins=30,
            title=f"Distribution of {selected_column}",
            labels={"x": selected_column, "y": "Frequency"}
        )

        st.plotly_chart(fig_hist, use_container_width=True)

        fig_box = px.box(
            y=valid_values,
            title=f"Box Plot of {selected_column}",
            labels={"y": selected_column}
        )

        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("This column contains no valid numerical values.")

# -------------------------------
# CORRELATION ANALYSIS
# -------------------------------

st.header("Correlation Analysis")

if numeric_df.shape[1] >= 2:
    correlation = numeric_df.corr()

    fig_corr = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1
    )

    st.plotly_chart(fig_corr, use_container_width=True)

else:
    st.info(
        "At least two numerical columns are required "
        "for correlation analysis."
    )

# -------------------------------
# AUTOMATIC INSIGHTS
# -------------------------------

st.header("💡 Automatic Data Insights")

st.write(
    "These observations are calculated from the uploaded dataset."
)

st.markdown(f"- The dataset contains **{len(df):,} rows** "
            f"and **{len(df.columns):,} columns**.")

missing_total = int(df.isna().sum().sum())
duplicate_total = int(df.duplicated().sum())

if missing_total:
    st.markdown(
        f"- **{missing_total:,} missing cells** were detected. "
        "Investigate their causes before deciding how to handle them."
    )
else:
    st.markdown("- No missing cells were detected.")

if duplicate_total:
    st.markdown(
        f"- **{duplicate_total:,} duplicate rows** were detected. "
        "Review them before deciding whether to remove them."
    )
else:
    st.markdown("- No duplicate rows were detected.")

if not numeric_df.empty:
    for column in numeric_df.columns:
        series = numeric_df[column].dropna()

        if series.empty:
            continue

        st.markdown(
            f"- **{column}:** mean = {series.mean():,.2f}, "
            f"median = {series.median():,.2f}, "
            f"minimum = {series.min():,.2f}, "
            f"maximum = {series.max():,.2f}."
        )

# -------------------------------
# DOWNLOAD ANALYSIS
# -------------------------------

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
