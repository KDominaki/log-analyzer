# app/controller.py
from typing import List

from tkinter import filedialog

from core.parser import parse_log_files
from core.analyzer import (
    count_codes_for_multiple_files,
    aggregate_total_counts,
    format_counts_for_display,
)


class Controller:
    def __init__(self, app):
        """
        app: instance of LogAnalyzerApp (from app.ui)
        """
        self.app = app
        self.selected_files: List[str] = []

    def select_files(self) -> None:
        """
        Open a file dialog to pick one or more .txt log files.
        """
        file_paths = filedialog.askopenfilenames(
            title="Select log files",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_paths:
            return  # user cancelled

        self.selected_files = list(file_paths)
        self.app.show_selected_files(self.selected_files)

    def analyze_files(self) -> None:
        """
        Parse selected files, count status codes, and send the report to the UI.
        """
        if not self.selected_files:
            self.app.show_error("No files selected. Please select log files first.")
            return

        codes_per_file = parse_log_files(self.selected_files)
        per_file_counts = count_codes_for_multiple_files(codes_per_file)
        total_counts = aggregate_total_counts(per_file_counts)
        report_text = format_counts_for_display(per_file_counts, total_counts)
        self.app.show_report(report_text)
