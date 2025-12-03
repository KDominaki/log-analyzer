import json
import re
from typing import List, Dict, Tuple


# Regex patterns
STATUS_PATTERN = re.compile(r"HttpStatus:\s*(\d{3})")
ERROR_MSG_PATTERN = re.compile(r'ErrorMsg:\s*(\{.*?\})\s*\}', re.DOTALL)


def _extract_error_msg(line: str) -> str:

    m = ERROR_MSG_PATTERN.search(line)
    if not m:
        return ""

    json_like = m.group(1)

    json_clean = json_like.replace('\\"', '"')

    try:
        obj = json.loads(json_clean)
    except Exception as e:
        error = f"Failed to parse JSON. Exception: " + str(e)

        return error

    return obj.get("detail", "").strip()


def parse_log_file(file_path: str) -> List[Tuple[int, str]]:
    """
    Returns a list of (status_code, error_message) tuples.
    Error message may be an empty string if nothing is provided.
    """
    results: List[Tuple[int, str]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                status_match = STATUS_PATTERN.search(line)
                if not status_match:
                    continue

                code = int(status_match.group(1))
                if 100 <= code <= 599:
                    msg = _extract_error_msg(line)
                    results.append((code, msg))
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading {file_path}: {e}")

    return results


def parse_log_files(file_paths: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    """
    For each file, return list of (status_code, error_message)
    """
    return {path: parse_log_file(path) for path in file_paths}
