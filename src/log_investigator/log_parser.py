
from pathlib import Path
from typing import List, Dict, Optional


def read_log_file(file_path: Path) -> List[str]:
    """
    Read the log file and return all lines as a list.
    """
    if not file_path.exists():
        raise FileNotFoundError("Log file not found: {}".format(file_path))

    return file_path.read_text(encoding="utf-8").splitlines()


def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    """
    Parse one log line into a dictionary.

    Expected format:
    Timestamp:12:00|IP:192.168.1.1|Status:200|ResponseTime:50ms
    """
    parts = line.split("|")
    data = {}

    for part in parts:
        if ":" not in part:
            return None

        key, value = part.split(":", 1)
        data[key.strip()] = value.strip()

    return data
