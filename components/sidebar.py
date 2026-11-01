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

    missing_strategy = st.sidebar.selectbox(
        "Handle Missing Values",
        ["None", "Drop Rows", "Mean", "Median", "Mode"]
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
        "missing_strategy": missing_strategy,
        "remove_duplicates": remove_duplicates,
    }