from pathlib import Path

from log_investigator.report_writer import summarize_issues, write_report


def test_summarize_issues_counts_each_type():
    issues = [
        "Line 2: Server error status detected -> 500",
        "Line 3: Invalid IP address -> abc.def",
        "Line 4: Server error status detected -> 500",
        "Line 4: Invalid response time -> abc",
        "Line 5: Missing field(s): ResponseTime -> Timestamp:12:04|IP:192.168.1.1|Status:500",
        "Line 7: Invalid log format -> random text not valid",
    ]

    summary = summarize_issues(issues)

    assert summary["Server error status"] == 2
    assert summary["Invalid IP address"] == 1
    assert summary["Invalid response time"] == 1
    assert summary["Missing field"] == 1
    assert summary["Invalid log format"] == 1
    assert summary["Other"] == 0


def test_write_report_creates_report_file(tmp_path):
    issues = [
        "Line 2: Server error status detected -> 500",
        "Line 3: Invalid IP address -> abc.def",
    ]

    output_path = tmp_path / "report.txt"
    source_path = Path("sample_logs/test.txt")

    write_report(issues, output_path, source_path)

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "LOG INVESTIGATION REPORT" in content
    assert "Source file: sample_logs/test.txt" in content
    assert "Total issues found: 2" in content
    assert "Summary by issue type:" in content
    assert "- Server error status: 1" in content
    assert "- Invalid IP address: 1" in content
    assert "Detailed issues:" in content
    assert "Line 2: Server error status detected -> 500" in content
    assert "Line 3: Invalid IP address -> abc.def" in content
