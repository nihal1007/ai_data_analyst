import pandas as pd

def generate_insights(df):
    insights = []

    # Dataset overview
    insights.append(
        f"The dataset contains {len(df)} rows and {len(df.columns)} columns."
    )

    # Missing values
    missing = df.isnull().sum()
    missing_columns = missing[missing > 0]

    if not missing_columns.empty:
        for column, count in missing_columns.items():
            percentage = (count / len(df)) * 100 if len(df) else 0

            insights.append(
                f"Data quality: '{column}' has {count} missing values "
                f"({percentage:.2f}% of rows)."
            )
    else:
        insights.append("Data quality: No missing values were found.")

    # Duplicate rows
    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:
        insights.append(
            f"Data quality: {duplicate_count} duplicate rows were found."
        )
    else:
        insights.append("Data quality: No duplicate rows were found.")

    # Numerical insights
    numeric_df = df.select_dtypes(include="number")

    for column in numeric_df.columns:
        series = numeric_df[column].dropna()

        if series.empty:
            insights.append(
                f"'{column}' has no valid numerical values to analyze."
            )
            continue

        mean_value = series.mean()
        median_value = series.median()

        insights.append(
            f"'{column}': mean = {mean_value:.2f}, "
            f"median = {median_value:.2f}, "
            f"minimum = {series.min():.2f}, "
            f"maximum = {series.max():.2f}."
        )

        if mean_value > median_value:
            insights.append(
                f"'{column}': the mean is greater than the median; "
                "a right-skewed distribution is possible."
            )
        elif mean_value < median_value:
            insights.append(
                f"'{column}': the mean is less than the median; "
                "a left-skewed distribution is possible."
            )

    if numeric_df.shape[1] >= 2:
        correlation = numeric_df.corr()

        for i, column_a in enumerate(correlation.columns):
            for column_b in correlation.columns[i + 1:]:
                value = correlation.loc[column_a, column_b]

                if pd.notna(value) and abs(value) >= 0.7:
                    direction = (
                        "positive" if value > 0 else "negative"
                    )

                    insights.append(
                        f"'{column_a}' and '{column_b}' show a strong "
                        f"{direction} correlation ({value:.2f}). "
                        "Correlation does not imply causation."
                    )

    return insights
