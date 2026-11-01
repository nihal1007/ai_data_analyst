import unittest
import pandas as pd

from services.eda_engine import run_eda

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