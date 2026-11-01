import pandas as pd

def get_statistical_summary(df):
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.agg(
        ["mean", "median", "std", "min", "max", "skew"]
    ).T.round(3)

def get_correlation_matrix(df):
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return pd.DataFrame()

    return numeric_df.corr().round(3)
