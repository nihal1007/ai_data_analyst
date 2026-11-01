import streamlit as st

def display_sidebar():
    st.sidebar.title("DataMind AI")
    st.sidebar.markdown("---")

    st.sidebar.subheader("Analysis Options")

    show_overview = st.sidebar.checkbox(
        "Dataset Overview",
        value=True
    )

    show_statistics = st.sidebar.checkbox(
        "Statistical Summary",
        value=True
    )

    show_visualizations = st.sidebar.checkbox(
        "Visualizations",
        value=True
    )

    show_insights = st.sidebar.checkbox(
        "Automatic Insights",
        value=True
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Cleaning")

    # Numerical column handling
    st.sidebar.markdown("**Numerical Columns**")

    numeric_strategy = st.sidebar.selectbox(
        "Fill numerical missing values",
        ["None", "Mean", "Median", "Mode", "Drop Rows"],
        key="numeric_strategy"
    )

    # Categorical and text column handling
    st.sidebar.markdown("**Categorical / Text Columns**")

    categorical_strategy = st.sidebar.selectbox(
        "Fill categorical missing values",
        ["None", "Mode", "Drop Rows"],
        key="categorical_strategy"
    )

    remove_duplicates = st.sidebar.checkbox(
        "Remove Duplicate Rows",
        value=False
    )

    return {
        "show_overview": show_overview,
        "show_statistics": show_statistics,
        "show_visualizations": show_visualizations,
        "show_insights": show_insights,
        "numeric_strategy": numeric_strategy,
        "categorical_strategy": categorical_strategy,
        "remove_duplicates": remove_duplicates,
    }