import streamlit as st
import pandas as pd

from components.charts import (
create_histogram,
create_box_plot,
create_correlation_heatmap,
)

def display_overview(overview):
    """Display key dataset metrics."""

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", overview["rows"])
    col2.metric("Columns", overview["columns"])
    col3.metric("Missing Cells", overview["missing_cells"])
    col4.metric("Duplicate Rows", overview["duplicate_rows"])

def display_missing_values(missing_values):
    """Display missing-value information."""

    st.subheader("Missing Value Analysis")

    if missing_values.empty:
        st.info("No columns found.")
        return

    st.dataframe(missing_values, use_container_width=True)

def display_numeric_summary(summary):
    """Display descriptive statistics."""

    st.subheader("Statistical Summary")

    if summary.empty:
        st.info("No numerical columns available.")
        return

    st.dataframe(summary, use_container_width=True)

def display_insights(insights):
    """Display automatically generated insights."""

    st.subheader("Automatic Insights")

    if not insights:
        st.info("No insights available.")
        return

    for insight in insights:
        st.markdown(f"- {insight}")

def display_visualizations(df):
    """Display interactive charts."""

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    st.subheader("Data Visualizations")

    if not numeric_columns:
        st.info("No numerical columns available for visualization.")
        return

    selected_column = st.selectbox(
        "Select a numerical column",
        numeric_columns,
    )

    col1, col2 = st.columns(2)

    try:
        with col1:
            st.plotly_chart(
                create_histogram(df, selected_column),
                use_container_width=True,
            )

        with col2:
            st.plotly_chart(
                create_box_plot(df, selected_column),
                use_container_width=True,
            )

    except ValueError as error:
        st.warning(str(error))

    heatmap = create_correlation_heatmap(df)

    if heatmap is not None:
        st.plotly_chart(
            heatmap,
            use_container_width=True,
        )
    else:
        st.info(
            "At least two numerical columns are needed "
            "for a correlation heatmap."
        )
