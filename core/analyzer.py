import os
from collections import Counter
from typing import Dict, List


def count_codes_for_file(codes: List[int]) -> Dict[int, int]:
    """
    Returns a dict of {status_code: count} for a single file.
    """
    return dict(Counter(codes))


def count_codes_for_multiple_files(
    codes_per_file: Dict[str, List[int]]
) -> Dict[str, Dict[int, int]]:

    per_file_counts: Dict[str, Dict[int, int]] = {}
    for file_path, codes in codes_per_file.items():
        per_file_counts[file_path] = count_codes_for_file(codes)
    return per_file_counts


def aggregate_total_counts(
    per_file_counts: Dict[str, Dict[int, int]]
) -> Dict[int, int]:
    """
    Sums counts across all files.
    """
    total_counter = Counter()
    for file_counts in per_file_counts.values():
        total_counter.update(file_counts)
    return dict(total_counter)


def format_counts_for_display(
    per_file_counts: Dict[str, Dict[int, int]],
    total_counts: Dict[int, int]
) -> str:
    """
    Returns a human-readable multi-line string for the UI.
    """
    lines: List[str] = []

    if not per_file_counts:
        return "No log files analyzed.\n"

    # Per-file section
    for file_path, counts in per_file_counts.items():
        file_name = os.path.basename(file_path)
        lines.append(f"File: {file_name}")
        if counts:
            for code in sorted(counts.keys()):
                lines.append(f"  {code}: {counts[code]}")
        else:
            lines.append("  No HttpStatus codes found.")
        lines.append("")  # blank line after each file

    # Total section
    lines.append("TOTAL (all files):")
    if total_counts:
        for code in sorted(total_counts.keys()):
            lines.append(f"  {code}: {total_counts[code]}")
    else:
        lines.append("  No HttpStatus codes found in any file.")

    return "\n".join(lines) + "\n"
