# app/controller.py
from typing import List

from tkinter import filedialog

from core.parser import parse_log_files
from core.analyzer import (
    analyze_multiple_files,
    aggregate_totals,
    format_results_for_display
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
        if not self.selected_files:
            self.app.show_error("No files selected. Please select log files first.")
            return

        files_data = parse_log_files(self.selected_files)
        per_file_results = analyze_multiple_files(files_data)
        total_results = aggregate_totals(per_file_results)

        report = format_results_for_display(per_file_results, total_results)
        self.app.show_report(report)