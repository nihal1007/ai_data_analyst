import unittest
import pandas as pd

from services.eda_engine import run_eda
from services.insights_engine import generate_insights

from components.charts import (
    create_histogram,
    create_box_plot,
    create_correlation_heatmap,
)
from services.data_cleaning import (
    remove_duplicate_rows,
    handle_missing_values,
    get_cleaning_summary,
)
from services.statistical_analysis import (
    get_statistical_summary,
    get_correlation_matrix,
)
from services.analysis import (
get_dataset_overview,
get_missing_values,
get_numeric_summary,
get_numeric_columns,
)

class TestDataAnalysis(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Name": ["A", "B", "C"],
            "Marks": [80, 90, 70],
            "Hours": [2, 4, 3],
            "City": ["Kochi", None, "Thrissur"],
        })

    def test_dataset_overview(self):
        result = get_dataset_overview(self.df)

        self.assertEqual(result["rows"], 3)
        self.assertEqual(result["columns"], 4)
        self.assertEqual(result["missing_cells"], 1)
        self.assertEqual(result["duplicate_rows"], 0)

    def test_missing_values(self):
        result = get_missing_values(self.df)

        self.assertEqual(result.loc["City", "Missing Values"], 1)
        self.assertEqual(
            result.loc["City", "Missing Percentage"], 33.33
        )

    def test_numeric_summary(self):
        result = get_numeric_summary(self.df)

        self.assertIn("Marks", result.index)
        self.assertIn("Hours", result.index)
        self.assertEqual(result.loc["Marks", "mean"], 80)

    def test_numeric_columns(self):
        result = get_numeric_columns(self.df)

        self.assertEqual(result, ["Marks", "Hours"])

    if __name__ == "__main__":
        unittest.main()
    def test_run_eda(self):
        result = run_eda(self.df)

        self.assertIn("overview", result)
        self.assertIn("missing_values", result)
        self.assertIn("numeric_summary", result)
        self.assertIn("numeric_columns", result)
        self.assertEqual(result["overview"]["rows"], 3)
    def test_statistical_summary(self):
        result = get_statistical_summary(self.df)
        self.assertIn("mean", result.columns)
        self.assertIn("median", result.columns)
        self.assertEqual(result.loc["Marks", "mean"], 80)

    def test_correlation_matrix(self):
        result = get_correlation_matrix(self.df)
        self.assertIn("Marks", result.columns)
        self.assertIn("Hours", result.columns)
        self.assertEqual(result.shape, (2, 2))



    def test_remove_duplicate_rows(self):
        df = pd.DataFrame({
            "Name": ["A", "A", "B"],
            "Marks": [80, 80, 90],
        })

        result = remove_duplicate_rows(df)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(df), 3)

    def test_handle_missing_values(self):
        result = handle_missing_values(self.df, strategy="mean")

        self.assertEqual(result["Marks"].isnull().sum(), 0)
        self.assertTrue(pd.isna(result.loc[1, "City"]))
        self.assertTrue(pd.isna(self.df.loc[1, "City"]))

    def test_cleaning_summary(self):
        cleaned_df = remove_duplicate_rows(self.df)

        result = get_cleaning_summary(self.df, cleaned_df)

        self.assertEqual(result["original_rows"], 3)
        self.assertEqual(result["cleaned_rows"], 3)
        self.assertEqual(result["removed_rows"], 0)


    def test_generate_insights(self):
        result = generate_insights(self.df)

        self.assertIsInstance(result, list)
        self.assertTrue(
            any("rows and" in insight for insight in result)
        )
        self.assertTrue(
            any("missing values" in insight for insight in result)
        )

    def test_generate_insights_without_numeric_columns(self):
        df = pd.DataFrame({
            "Name": ["A", "B"],
            "City": ["Kochi", "Thrissur"],
        })

        result = generate_insights(df)

        self.assertIsInstance(result, list)
        self.assertTrue(
            any("No missing values" in insight for insight in result)
        )

    def test_create_histogram(self):
        result = create_histogram(self.df, "Marks")

        self.assertIsNotNone(result)
        self.assertEqual(result.layout.title.text, "Distribution of Marks")

    def test_create_box_plot(self):
        result = create_box_plot(self.df, "Marks")

        self.assertIsNotNone(result)
        self.assertEqual(result.layout.title.text, "Box Plot of Marks")

    def test_create_correlation_heatmap(self):
        result = create_correlation_heatmap(self.df)

        self.assertIsNotNone(result)
