from pathlib import Path

from log_investigator.report_writer import (
    summarize_issues_by_type,
    summarize_issues_by_severity,
    write_report,
)


def test_summarize_issues_by_type_counts_each_type():
    issues = [
        "[CRITICAL] Line 2: Server error status detected -> 500",
        "[ERROR] Line 3: Invalid IP address -> abc.def",
        "[CRITICAL] Line 4: Server error status detected -> 500",
        "[ERROR] Line 4: Invalid response time -> abc",
        "[ERROR] Line 5: Missing field(s): ResponseTime -> Timestamp:12:04|IP:192.168.1.1|Status:500",
        "[ERROR] Line 7: Invalid log format -> random text not valid",
        "[WARNING] Line 8: High response time -> 1500ms (threshold: 1000ms)",
    ]

    summary = summarize_issues_by_type(issues)

    assert summary["Server error status"] == 2
    assert summary["Invalid IP address"] == 1
    assert summary["Invalid response time"] == 1
    assert summary["High response time"] == 1
    assert summary["Missing field"] == 1
    assert summary["Invalid log format"] == 1
    assert summary["Other"] == 0


def test_summarize_issues_by_severity_counts_each_level():
    issues = [
        "[CRITICAL] Line 2: Server error status detected -> 500",
        "[ERROR] Line 3: Invalid IP address -> abc.def",
        "[CRITICAL] Line 4: Server error status detected -> 500",
        "[ERROR] Line 4: Invalid response time -> abc",
        "[WARNING] Line 8: High response time -> 1500ms (threshold: 1000ms)",
    ]

    summary = summarize_issues_by_severity(issues)

    assert summary["CRITICAL"] == 2
    assert summary["ERROR"] == 2
    assert summary["WARNING"] == 1


def test_write_report_creates_report_file(tmp_path):
    issues = [
        "[CRITICAL] Line 2: Server error status detected -> 500",
        "[ERROR] Line 3: Invalid IP address -> abc.def",
        "[WARNING] Line 8: High response time -> 1500ms (threshold: 1000ms)",
    ]

    output_path = tmp_path / "report.txt"
    source_path = Path("sample_logs/test.txt")

    write_report(issues, output_path, source_path)

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "LOG INVESTIGATION REPORT" in content
    assert "Source file: sample_logs/test.txt" in content
    assert "Total issues found: 3" in content
    assert "Summary by severity:" in content
    assert "- CRITICAL: 1" in content
    assert "- ERROR: 1" in content
    assert "- WARNING: 1" in content
    assert "Summary by issue type:" in content
    assert "- Server error status: 1" in content
    assert "- Invalid IP address: 1" in content
    assert "- High response time: 1" in content
    assert "Detailed issues:" in content
    assert "[CRITICAL] Line 2: Server error status detected -> 500" in content
    assert "[ERROR] Line 3: Invalid IP address -> abc.def" in content
    assert "[WARNING] Line 8: High response time -> 1500ms (threshold: 1000ms)" in content
