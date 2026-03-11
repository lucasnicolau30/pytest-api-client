"""
CSV handling for test results.
"""

import csv
import os


def initialize_csv(csv_file):
    """
    Create and initialize CSV file with headers.
    
    Args:
        csv_file: Path to the CSV file
    """
    # Create directory if not exists
    directory = os.path.dirname(csv_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Scenario",
            "Parameters",
            "Expected Status",
            "Actual Status",
            "Average Time (s)",
            "Min Time (s)",
            "Max Time (s)",
            "Success"
        ])


def append_result(csv_file, description, params, expected_status, actual_status, average_time, min_time, max_time, success):
    """
    Append a test result row to CSV.
    
    Args:
        csv_file: Path to CSV file
        description: Scenario description
        params: Request parameters dict
        expected_status: Expected HTTP status
        actual_status: Actual HTTP status
        average_time: Average response time
        min_time: Minimum response time
        max_time: Maximum response time
        success: Whether test passed
    """
    with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            description,
            str(params),
            expected_status,
            actual_status,
            round(average_time, 3),
            round(min_time, 3),
            round(max_time, 3),
            "OK" if success else "FAILED"
        ])