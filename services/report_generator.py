from datetime import datetime


def generate_report(df, overview, insights):
    report = []

    report.append("=" * 50)
    report.append("           DATAMIND AI - ANALYSIS REPORT")
    report.append("=" * 50)

    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    report.append("\n1. DATASET OVERVIEW")
    report.append("-" * 30)
    report.append(f"Total Rows: {overview['rows']}")
    report.append(f"Total Columns: {overview['columns']}")
    report.append(f"Missing Cells: {overview['missing_cells']}")
    report.append(f"Duplicate Rows: {overview['duplicate_rows']}")

    report.append("\n2. COLUMN NAMES")
    report.append("-" * 30)

    for column in df.columns:
        report.append(str(column))

    report.append("\n3. AUTOMATIC INSIGHTS")
    report.append("-" * 30)

    if insights:
        for index, insight in enumerate(insights, start=1):
            report.append(f"{index}. {insight}")
    else:
        report.append("No insights available.")

    report.append("\n" + "=" * 50)
    report.append("          END OF REPORT")
    report.append("=" * 50)

    return "\n".join(report)