
import re
from typing import List, Dict

# Regex to capture a 3-digit status code after "HttpStatus:"
STATUS_PATTERN = re.compile(r"HttpStatus:\s*(\d{3})")

def parse_log_file(file_path: str) -> List[int]:
    """
    Reads a single log file and returns a list of status codes (as ints)
    found in lines containing 'HttpStatus:'.
    """
    codes: List[int] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = STATUS_PATTERN.search(line)
                if match:
                    code_str = match.group(1)
                    code = int(code_str)

                    # Optionally ensure it's an HTTP status (100–599)
                    if 100 <= code <= 599:
                        codes.append(code)
    except (OSError, UnicodeDecodeError) as e:
        # You could log this somewhere; for now just print
        print(f"Error reading {file_path}: {e}")

    return codes


def parse_log_files(file_paths: List[str]) -> Dict[str, List[int]]:
    """
    Reads multiple log files and returns a mapping:
    {
      "path/to/file1.txt": [200, 404, 500, ...],
      "path/to/file2.txt": [401, 401, 406, ...],
      ...
    }
    """
    result: Dict[str, List[int]] = {}
    for path in file_paths:
        result[path] = parse_log_file(path)
    return result

