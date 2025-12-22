
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
import re

from app.controller import Controller


class LogAnalyzerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Log File Analyzer")
        self.root.geometry("850x550")

        self.controller = Controller(self)

        self._build_ui()

    def _build_ui(self):
        # Top frame with buttons
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(side="top", fill="x")

        # Select mobile logs button
        self.select_button = ttk.Button(
            top_frame,
            text="Select Mobile logs",
            command=lambda:
            (self.controller.set_mode("txt"),
             self.controller.select_files())
        )
        self.select_button.pack(side="left", padx=(0, 10))

        # Select API logs button
        self.select_button = ttk.Button(
            top_frame,
            text="Select API logs",
            command=lambda:
            (self.controller.set_mode("csv"),
             self.controller.select_files())
        )
        self.select_button.pack(side="left", padx=(0, 10))

        # Analyze button
        self.analyze_button = ttk.Button(
            top_frame,
            text="Analyze",
            command=self.controller.analyze_files
        )
        self.analyze_button.pack(side="left")

        # Clear output button
        self.clear_button = ttk.Button(
            top_frame,
            text="Clear output",
            command=self.clear_report
        )
        self.clear_button.pack(side="right")

        # Label showing selected files info
        self.selected_label_var = tk.StringVar(value="No files selected.")
        self.selected_label = ttk.Label(
            self.root,
            textvariable=self.selected_label_var,
            padding=(10, 5)
        )
        self.selected_label.pack(side="top", anchor="w")

        # Text area for report
        text_frame = ttk.Frame(self.root, padding=10)
        text_frame.pack(side="top", fill="both", expand=True)

        self.report_text = tk.Text(text_frame, wrap="word")
        self.report_text.pack(side="left", fill="both", expand=True)
        self.report_text.tag_configure("bold_code", font=("TkDefaultFont", 10, "bold"))

        self.report_text.config(state="disabled")

        # Scrollbar for text
        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.report_text.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.report_text.configure(yscrollcommand=scrollbar.set)

        # Bottom frame for version + copy button
        bottom_frame = ttk.Frame(self.root, padding=(10, 5))
        bottom_frame.pack(side="bottom", fill="x")

        # Version label (left)
        version = self.controller.read_version()
        self.version_label = ttk.Label(
            bottom_frame,
            text=f"Version: {version}"
        )
        self.version_label.pack(side="left")

        # Copy output button (right)
        self.copy_button = ttk.Button(
            bottom_frame,
            text="Copy output",
            command=self.copy_output
        )
        self.copy_button.pack(side="right")

    def run(self):
        self.root.mainloop()

    # Methods used by controller:

    def show_selected_files(self, file_paths: List[str]) -> None:
        if not file_paths:
            self.selected_label_var.set("No files selected.")
            return

        # Show only file names or full paths – here we use count + first file
        if len(file_paths) == 1:
            msg = f"Selected 1 file"
        else:
            msg = f"Selected {len(file_paths)} files."
        self.selected_label_var.set(msg)

    def show_report(self, report_text: str) -> None:
        self.report_text.config(state="normal")  # enable editing
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report_text)
        self._apply_syntax_highlighting()
        self.report_text.config(state="disabled")  # disable editing

    def clear_report(self) -> None:
        self.report_text.config(state="normal")
        self.report_text.delete(1.0, tk.END)
        self.report_text.config(state="disabled")

    def _apply_syntax_highlighting(self) -> None:
        self.report_text.tag_remove("bold_code", "1.0", tk.END)

        content = self.report_text.get("1.0", "end-1c")
        lines = content.split("\n")

        # Match 3-digit codes at start of line (optionally after spaces) followed by a colon
        code_pattern = re.compile(r"^\s*(\d{3})(?=:)")

        for line_index, line in enumerate(lines, start=1):
            match = code_pattern.search(line)
            if not match:
                continue

            # Only highlight the code part (group 1), not the spaces
            start_col = match.start(1)
            end_col = match.end(1)

            start_index = f"{line_index}.{start_col}"
            end_index = f"{line_index}.{end_col}"

            self.report_text.tag_add("bold_code", start_index, end_index)

    def show_error(self, message: str) -> None:
        messagebox.showerror("Error", message)

    def copy_output(self) -> None:
        """Copy the current output text to the clipboard."""
        content = self.report_text.get("1.0", tk.END).strip()
        if not content:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied", "Output copied to clipboard.")

