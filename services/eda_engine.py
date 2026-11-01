from services.analysis import (
get_dataset_overview,
get_missing_values,
get_numeric_summary,
get_numeric_columns,
)

def run_eda(df):

    results = {
        "overview": get_dataset_overview(df),
        "missing_values": get_missing_values(df),
        "numeric_summary": get_numeric_summary(df),
        "numeric_columns": get_numeric_columns(df),
    }

    return results