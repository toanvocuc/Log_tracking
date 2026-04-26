from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    line: int
    issue_type: str
    severity: str
    message: str
    value: Optional[str]
    raw_line: str
