import pandas as pd

def remove_duplicate_rows(df):
    """Return a copy of the dataset with duplicate rows removed."""

    return df.drop_duplicates().copy()

def handle_missing_values(df, strategy="none"):
    """Handle missing values using a selected strategy."""

    cleaned_df = df.copy()

    if strategy == "none":
        return cleaned_df

    elif strategy == "drop":
        return cleaned_df.dropna().copy()

    elif strategy == "mean":
        numeric_columns = cleaned_df.select_dtypes(
            include="number"
        ).columns

        cleaned_df[numeric_columns] = cleaned_df[
            numeric_columns
        ].fillna(cleaned_df[numeric_columns].mean())

        return cleaned_df

    elif strategy == "median":
        numeric_columns = cleaned_df.select_dtypes(
            include="number"
        ).columns

        cleaned_df[numeric_columns] = cleaned_df[
            numeric_columns
        ].fillna(cleaned_df[numeric_columns].median())

        return cleaned_df

    elif strategy == "mode":
        for column in cleaned_df.columns:
            modes = cleaned_df[column].mode(dropna=True)

            if not modes.empty:
                cleaned_df[column] = cleaned_df[column].fillna(
                    modes.iloc[0]
                )

        return cleaned_df

    else:
        raise ValueError(
            "Invalid strategy. Choose none, drop, mean, median, or mode."
        )

def get_cleaning_summary(original_df, cleaned_df):
    """Summarize the changes made during cleaning."""

    return {
        "original_rows": len(original_df),
        "cleaned_rows": len(cleaned_df),
        "removed_rows": len(original_df) - len(cleaned_df),
        "original_missing_cells": int(
            original_df.isnull().sum().sum()
        ),
        "cleaned_missing_cells": int(
            cleaned_df.isnull().sum().sum()
        ),
        "remaining_duplicates": int(cleaned_df.duplicated().sum()),
    }
def handle_missing_values_by_type(
    df,
    numeric_strategy="none",
    categorical_strategy="none"
    ):
    import pandas as pd

    cleaned_df = df.copy()

    numeric_columns = cleaned_df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = cleaned_df.select_dtypes(
        exclude="number"
    ).columns

    # Handle numerical columns
    if numeric_strategy == "drop":
        cleaned_df = cleaned_df.dropna(
            subset=list(numeric_columns)
        )

    elif numeric_strategy in ["mean", "median", "mode"]:
        for column in numeric_columns:
            if cleaned_df[column].isna().any():
                if numeric_strategy == "mean":
                    fill_value = cleaned_df[column].mean()
                elif numeric_strategy == "median":
                    fill_value = cleaned_df[column].median()
                else:
                    modes = cleaned_df[column].mode()
                    if modes.empty:
                        continue
                    fill_value = modes.iloc[0]

                if pd.notna(fill_value):
                    cleaned_df[column] = cleaned_df[column].fillna(
                        fill_value
                    )

    # Handle categorical and text columns
    if categorical_strategy == "drop":
        cleaned_df = cleaned_df.dropna(
            subset=list(categorical_columns)
        )

    elif categorical_strategy == "mode":
        for column in categorical_columns:
            if cleaned_df[column].isna().any():
                modes = cleaned_df[column].mode(dropna=True)

                if not modes.empty:
                    cleaned_df[column] = cleaned_df[column].fillna(
                        modes.iloc[0]
                    )

    return cleaned_df