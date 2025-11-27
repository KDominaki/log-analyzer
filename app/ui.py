# app/ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from app.controller import Controller


class LogAnalyzerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Log Status Analyzer")
        self.root.geometry("800x500")

        self.controller = Controller(self)

        self._build_ui()

    def _build_ui(self):
        # Top frame with buttons
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Select files button
        self.select_button = ttk.Button(
            top_frame,
            text="Select log files",
            command=self.controller.select_files
        )
        self.select_button.pack(side=tk.LEFT, padx=(0, 10))

        # Analyze button
        self.analyze_button = ttk.Button(
            top_frame,
            text="Analyze",
            command=self.controller.analyze_files
        )
        self.analyze_button.pack(side=tk.LEFT)

        # Label showing selected files info
        self.selected_label_var = tk.StringVar(value="No files selected.")
        self.selected_label = ttk.Label(
            self.root,
            textvariable=self.selected_label_var,
            padding=(10, 5)
        )
        self.selected_label.pack(side=tk.TOP, anchor="w")

        # Text area for report
        text_frame = ttk.Frame(self.root, padding=10)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.report_text = tk.Text(text_frame, wrap="word")
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for text
        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.report_text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text.configure(yscrollcommand=scrollbar.set)

    def run(self):
        self.root.mainloop()

    # Methods used by controller:

    def show_selected_files(self, file_paths: List[str]) -> None:
        if not file_paths:
            self.selected_label_var.set("No files selected.")
            return

        # Show only file names or full paths – here we use count + first file
        if len(file_paths) == 1:
            msg = f"Selected 1 file: {file_paths[0]}"
        else:
            msg = f"Selected {len(file_paths)} files. First: {file_paths[0]}"
        self.selected_label_var.set(msg)

    def show_report(self, report_text: str) -> None:
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report_text)

    def show_error(self, message: str) -> None:
        messagebox.showerror("Error", message)
