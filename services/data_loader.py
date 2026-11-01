import pandas as pd


def load_dataset(uploaded_file):
    """Load a CSV or Excel file into a Pandas DataFrame."""

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        else:
            raise ValueError(
                "Unsupported file format. Upload a CSV or XLSX file."
            )

        if df.empty:
            raise ValueError("The uploaded dataset is empty.")

        if len(df.columns) == 0:
            raise ValueError("No columns were found in the dataset.")

        return df

    except (ValueError, pd.errors.ParserError):
        raise

    except Exception as error:
        raise ValueError(
            f"Could not read the dataset: {error}"
        ) from error