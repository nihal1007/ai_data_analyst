import pandas as pd
import plotly.express as px

def create_histogram(df, column):
    """Create a histogram for a numerical column."""

    if column not in df.columns:
        raise ValueError(f"Column '{column}' was not found.")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numerical.")

    data = df[column].dropna()

    if data.empty:
        raise ValueError(f"Column '{column}' has no valid values.")

    return px.histogram(
        df,
        x=column,
        title=f"Distribution of {column}",
        labels={column: column},
    )

def create_box_plot(df, column):
    """Create a box plot for a numerical column."""

    if column not in df.columns:
        raise ValueError(f"Column '{column}' was not found.")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numerical.")

    data = df[column].dropna()

    if data.empty:
        raise ValueError(f"Column '{column}' has no valid values.")

    return px.box(
        df,
        y=column,
        title=f"Box Plot of {column}",
    )

def create_correlation_heatmap(df):
    """Create a correlation heatmap for numerical columns."""

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    correlation = numeric_df.corr()

    return px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Correlation Heatmap",
    )