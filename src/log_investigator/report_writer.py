from pathlib import Path
from typing import List, Dict


def summarize_issues_by_type(issues: List[str]) -> Dict[str, int]:
    summary = {
        "Server error status": 0,
        "Invalid IP address": 0,
        "Invalid response time": 0,
        "High response time": 0,
        "Missing field": 0,
        "Invalid log format": 0,
        "Other": 0,
    }

    for issue in issues:
        if "Server error status detected" in issue:
            summary["Server error status"] += 1
        elif "Invalid IP address" in issue:
            summary["Invalid IP address"] += 1
        elif "Invalid response time" in issue:
            summary["Invalid response time"] += 1
        elif "High response time" in issue:
            summary["High response time"] += 1
        elif "Missing field(s)" in issue:
            summary["Missing field"] += 1
        elif "Invalid log format" in issue:
            summary["Invalid log format"] += 1
        else:
            summary["Other"] += 1

    return summary


def summarize_issues_by_severity(issues: List[str]) -> Dict[str, int]:
    summary = {
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
    }

    for issue in issues:
        if issue.startswith("[WARNING]"):
            summary["WARNING"] += 1
        elif issue.startswith("[ERROR]"):
            summary["ERROR"] += 1
        elif issue.startswith("[CRITICAL]"):
            summary["CRITICAL"] += 1

    return summary


def write_report(issues: List[str], output_path: Path, source_path: Path) -> None:
    type_summary = summarize_issues_by_type(issues)
    severity_summary = summarize_issues_by_severity(issues)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        file.write("LOG INVESTIGATION REPORT\n")
        file.write("=" * 50 + "\n")
        file.write("Source file: {}\n".format(source_path))
        file.write("Total issues found: {}\n\n".format(len(issues)))

        file.write("Summary by severity:\n")
        for severity, count in severity_summary.items():
            if count > 0:
                file.write("- {}: {}\n".format(severity, count))

        file.write("\nSummary by issue type:\n")
        for issue_type, count in type_summary.items():
            if count > 0:
                file.write("- {}: {}\n".format(issue_type, count))

        file.write("\nDetailed issues:\n")
        for issue in issues:
            file.write(issue + "\n")
