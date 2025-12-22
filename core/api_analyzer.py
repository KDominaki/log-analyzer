# core/api_analyzer.py
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List

from core.api_parser import ApiLogEntry


@dataclass
class ApiAnalysisResult:
    true_count: int
    false_count: int
    false_msgs: Dict[str, int]  # msg -> count


def analyze_api_entries(entries: List[ApiLogEntry]) -> ApiAnalysisResult:
    """
    Analyze a single file's entries:
      - count success True / False
      - for False, count messages
    """
    true_count = 0
    false_count = 0
    false_msgs: Dict[str, int] = {}

    for e in entries:
        if e.success:
            true_count += 1
        else:
            false_count += 1
            msg_key = e.msg.strip()  # may be empty -> ""
            false_msgs[msg_key] = false_msgs.get(msg_key, 0) + 1

    return ApiAnalysisResult(true_count=true_count, false_count=false_count, false_msgs=false_msgs)


def analyze_api_files(
    per_file_entries: Dict[str, List[ApiLogEntry]]
) -> Dict[str, ApiAnalysisResult]:
    """
    Analyze multiple files:
      { file_path: ApiAnalysisResult, ... }
    """
    return {path: analyze_api_entries(entries) for path, entries in per_file_entries.items()}


def aggregate_api_totals(
    per_file_results: Dict[str, ApiAnalysisResult]
) -> ApiAnalysisResult:
    """
    Aggregate totals across all files.
    """
    total_true = 0
    total_false = 0
    total_false_msgs: Dict[str, int] = {}

    for res in per_file_results.values():
        total_true += res.true_count
        total_false += res.false_count
        for msg, cnt in res.false_msgs.items():
            total_false_msgs[msg] = total_false_msgs.get(msg, 0) + cnt

    return ApiAnalysisResult(true_count=total_true, false_count=total_false, false_msgs=total_false_msgs)


def format_api_results_for_display(
    per_file_results: Dict[str, ApiAnalysisResult],
    totals: ApiAnalysisResult
) -> str:
    """
    Human-readable output consistent with your TXT output style.
    Shows:
      - True / False counts
      - For False: message breakdown + counts
    """
    lines: List[str] = []

    if not per_file_results:
        return "No API CSV files analyzed.\n"

    for path, res in per_file_results.items():
        file_name = os.path.basename(path)
        lines.append(f"File: {file_name}")
        lines.append(f"  Success True: {res.true_count}")
        lines.append(f"  Success False: {res.false_count}")

        if res.false_count > 0:
            # Show message breakdown (sorted by count desc, then message)
            items = sorted(res.false_msgs.items(), key=lambda x: (-x[1], x[0]))
            for msg, count in items:
                times = "time" if count == 1 else "times"
                if msg == "":
                    lines.append(f"      (no msg) — {count} {times}")
                else:
                    lines.append(f'      "{msg}" — {count} {times}')

        lines.append("")

    lines.append("TOTAL (across all files):")
    lines.append(f"  Success True: {totals.true_count}")
    lines.append(f"  Success False: {totals.false_count}")

    if totals.false_count > 0:
        items = sorted(totals.false_msgs.items(), key=lambda x: (-x[1], x[0]))
        for msg, count in items:
            times = "time" if count == 1 else "times"
            if msg == "":
                lines.append(f"      (no msg) — {count} {times}")
            else:
                lines.append(f'      "{msg}" — {count} {times}')

    lines.append("")
    return "\n".join(lines)
