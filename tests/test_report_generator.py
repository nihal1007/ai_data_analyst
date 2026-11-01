import unittest
import pandas as pd

from services.analysis import get_dataset_overview
from services.insights_engine import generate_insights
from services.report_generator import generate_report


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Name": ["Arun", "Meera", "John"],
            "Marks": [80, 90, 70]
        })

        self.overview = get_dataset_overview(self.df)
        self.insights = generate_insights(self.df)

    def test_report_is_generated(self):
        report = generate_report(
            self.df,
            self.overview,
            self.insights
        )

        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)

    def test_report_contains_dataset_overview(self):
        report = generate_report(
            self.df,
            self.overview,
            self.insights
        )

        self.assertIn("Total Rows: 3", report)
        self.assertIn("Total Columns: 2", report)

    def test_report_contains_column_names(self):
        report = generate_report(
            self.df,
            self.overview,
            self.insights
        )

        self.assertIn("Name", report)
        self.assertIn("Marks", report)


if __name__ == "__main__":
    unittest.main()