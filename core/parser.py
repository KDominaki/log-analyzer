
import re
from typing import List, Dict, Tuple

# Regex patterns
STATUS_PATTERN = re.compile(r"HttpStatus:\s*(\d{3})")
ERROR_PATTERN = re.compile(r"ErrorMsg:\s*(.*?)\s*(?=[},]|$)")

def parse_log_file(file_path: str) -> List[Tuple[int, str]]:
    """
    Returns a list of (status_code, error_message) tuples.
    Error message may be empty string if nothing is provided.
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
                    # Try to extract error message
                    error_match = ERROR_PATTERN.search(line)
                    if error_match:
                        msg = error_match.group(1).strip()
                    else:
                        msg = ""

                    results.append((code, msg))

    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading {file_path}: {e}")

    return results


def parse_log_files(file_paths: List[str]) -> Dict[str, List[Tuple[int, str]]]:
    """
    For each file, return list of (status_code, error_message)
    """
    return {path: parse_log_file(path) for path in file_paths}


