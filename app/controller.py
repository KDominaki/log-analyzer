import os
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
        self.mode = "txt"
        self.selected_files: List[str] = []

    def set_mode(self, mode):
        self.mode = mode

    def select_files(self) -> None:
        if self.mode == "txt":

            file_paths = filedialog.askopenfilenames(
                title="Select log files",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_paths:
                return  # user cancelled

            self.selected_files = list(file_paths)
            self.app.show_selected_files(self.selected_files)

        elif self.mode == "csv":
            file_paths = filedialog.askopenfilenames(
                title="Select log files",
                filetypes=[("Text files", "*.csv"), ("All files", "*.*")]
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

    def read_version(self):
        version_file = os.path.join(os.path.dirname(__file__), "version.txt")
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                # Expected format: version = "0.1.0"
                if "version" in content:
                    return content.split("=")[1].strip().strip('"')
        except Exception:
            return "Unknown"

        return "Unknown"