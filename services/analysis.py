import pandas as pd
import numpy as np

def get_dataset_overview(df):
    """Get basic information about the dataset."""
    return {
    "rows": len(df),
    "columns": len(df.columns),
    "missing_cells": int(df.isnull().sum().sum()),
    "duplicate_rows": int(df.duplicated().sum()),
    }

def get_missing_values(df):
    """Calculate missing values and percentages."""
    return pd.DataFrame({
    "Missing Values": df.isnull().sum(),
    "Missing Percentage": (df.isnull().mean() * 100).round(2),
    })

def get_numeric_summary(df):
    """Generate descriptive statistics for numerical columns."""
    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.describe().T.round(2)

def get_numeric_columns(df):
    """Get the names of numerical columns."""
    return df.select_dtypes(include=np.number).columns.tolist()
