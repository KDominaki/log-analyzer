import os
from typing import Dict, List, Tuple


def analyze_file(entries: List[Tuple[int, str]]) -> Dict[int, Dict[str, int]]:
    """
    For a single file:
    Return structure:
    {
        406: { "Invalid payload format": 2 },
        401: { "": 3 }
    }
    """
    result: Dict[int, Dict[str, int]] = {}

    for status, msg in entries:
        if status not in result:
            result[status] = {}
        if msg not in result[status]:
            result[status][msg] = 0
        result[status][msg] += 1

    return result


def analyze_multiple_files(
    files_data: Dict[str, List[Tuple[int, str]]]
) -> Dict[str, Dict[int, Dict[str, int]]]:

    return {file: analyze_file(entries) for file, entries in files_data.items()}


def aggregate_totals(
    per_file_results: Dict[str, Dict[int, Dict[str, int]]]
) -> Dict[int, Dict[str, int]]:
    """
    Sum all counts across files:

    {
      406: { "Invalid payload": 12, "User not authorised": 3 },
      401: { "": 5 }
    }
    """
    totals: Dict[int, Dict[str, int]] = {}

    for file_result in per_file_results.values():
        for status, msg_map in file_result.items():
            if status not in totals:
                totals[status] = {}

            for msg, count in msg_map.items():
                totals[status][msg] = totals[status].get(msg, 0) + count

    return totals

def format_results_for_display(
    per_file_results: Dict[str, Dict[int, Dict[str, int]]],
    total_results: Dict[int, Dict[str, int]]
) -> str:

    lines: List[str] = []

    if not per_file_results:
        return "No log files analyzed.\n"

    # Per-file section
    for path, stats in per_file_results.items():
        file_name = os.path.basename(path)
        lines.append(f"File: {file_name}")

        if not stats:
            lines.append("  No HttpStatus codes found.\n")
            continue

        for status in sorted(stats.keys()):
            msg_map = stats[status]
            total_count = sum(msg_map.values())
            occ_word = "occurrence" if total_count == 1 else "occurrences"

            lines.append(f"  {status}: {total_count} {occ_word}")

            for msg, count in msg_map.items():
                times = "time" if count == 1 else "times"
                if msg == "":
                    lines.append(f"      (no error message) — {count} {times}")
                else:
                    lines.append(f'      "{msg}" — {count} {times}')

        lines.append("")  # blank line

    # Total section
    lines.append("TOTAL (across all files):")

    for status in sorted(total_results.keys()):
        msg_map = total_results[status]
        total_count = sum(msg_map.values())
        occ_word = "occurrence" if total_count == 1 else "occurrences"

        lines.append(f"  {status}: {total_count} {occ_word}")

        for msg, count in msg_map.items():
            times = "time" if count == 1 else "times"
            if msg == "":
                lines.append(f"      (no error message) — {count} {times}")
            else:
                lines.append(f'      "{msg}" — {count} {times}')

    lines.append("")
    return "\n".join(lines)
