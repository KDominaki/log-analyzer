
import csv
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ApiLogEntry:
    """
    Represents one row from the API CSV log.
    success: True/False
    msg: the message
    """
    success: bool
    msg: str


def _to_bool(value: str) -> Optional[bool]:
    """
    Convert string -> bool.
    Accepts: True/False (any casing), 1/0, yes/no.
    Returns None if not recognized.
    """
    if value is None:
        return None
    v = value.strip().lower()
    if v in ("true", "1", "yes", "y"):
        return True
    if v in ("false", "0", "no", "n"):
        return False
    return None


def parse_api_csv_file(file_path: str, *, delimiter: str = ";") -> List[ApiLogEntry]:
    """
    Parse a single API CSV log file.

    Expected columns include:
      - success
      - msg

    Notes:
      - delimiter is ';' (based on your example)
      - values may be quoted
      - rows with missing/invalid 'success' are skipped
    """
    entries: List[ApiLogEntry] = []

    # utf-8-sig handles BOM if present
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        if not reader.fieldnames:
            return entries

        # normalize headers to lower-case for robust access
        # but keep row dict keys as-is; we'll access using a helper
        headers_lower = {h.lower(): h for h in reader.fieldnames if h is not None}

        def get_col(row: dict, col_name: str) -> str:
            key = headers_lower.get(col_name.lower())
            return row.get(key, "") if key else ""

        for row in reader:
            success_raw = get_col(row, "success")
            success_val = _to_bool(success_raw)
            if success_val is None:
                # skip rows that don't have a valid success value
                continue

            msg = get_col(row, "msg").strip()
            entries.append(ApiLogEntry(success=success_val, msg=msg))

    return entries


def parse_api_csv_files(
    file_paths: List[str], *, delimiter: str = ";"
) -> Dict[str, List[ApiLogEntry]]:
    """
    Parse multiple API CSV files into:
      { file_path: [ApiLogEntry, ...], ... }
    """
    result: Dict[str, List[ApiLogEntry]] = {}
    for path in file_paths:
        try:
            result[path] = parse_api_csv_file(path, delimiter=delimiter)
        except (OSError, UnicodeDecodeError, csv.Error) as e:
            # If you prefer, you can raise instead. For now we store empty results.
            print(f"Error reading CSV {path}: {e}")
            result[path] = []
    return result
