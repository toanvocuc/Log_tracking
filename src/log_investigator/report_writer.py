from pathlib import Path
from typing import List


def write_report(issues: List[str], output_path: Path) -> None:
    """
    Write detected issues into the report file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        file.write("LOG INVESTIGATION REPORT\n")
        file.write("=" * 50 + "\n")
        file.write("Total issues found: {}\n\n".format(len(issues)))

        for issue in issues:
            file.write(issue + "\n")
