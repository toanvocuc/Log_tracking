from log_investigator.log_analyzer import (
    is_valid_ip,
    is_valid_response_time,
    analyze_logs,
)


TEST_RULES = {
    "fail_status_codes": [500, 502, 503],
    "response_time_threshold_ms": 1000,
    "required_fields": ["Timestamp", "IP", "Status", "ResponseTime"],
    "fail_on_invalid_ip": True,
    "fail_on_invalid_format": True,
    "fail_on_missing_fields": True,
}


def test_is_valid_ip_with_valid_ip():
    assert is_valid_ip("192.168.1.1") is True
    assert is_valid_ip("8.8.8.8") is True


def test_is_valid_ip_with_invalid_ip():
    assert is_valid_ip("abc.def") is False
    assert is_valid_ip("999.999.999.999") is False


def test_is_valid_response_time_with_valid_value():
    assert is_valid_response_time("50ms") is True
    assert is_valid_response_time("1200ms") is True


def test_is_valid_response_time_with_invalid_value():
    assert is_valid_response_time("abc") is False
    assert is_valid_response_time("1200") is False
    assert is_valid_response_time("ms") is False


def test_analyze_logs_detects_expected_issues():
    lines = [
        "Timestamp:12:00|IP:192.168.1.1|Status:200|ResponseTime:50ms",
        "Timestamp:12:01|IP:abc.def|Status:200|ResponseTime:30ms",
        "Timestamp:12:02|IP:8.8.8.8|Status:500|ResponseTime:abc",
        "Timestamp:12:03|IP:192.168.1.1|Status:500",
        "random text not valid",
    ]

    issues = analyze_logs(lines, TEST_RULES)

    assert len(issues) == 5
    assert any("Invalid IP address" in issue for issue in issues)
    assert any("Server error status detected" in issue for issue in issues)
    assert any("Invalid response time" in issue for issue in issues)
    assert any("Missing field(s)" in issue for issue in issues)
    assert any("Invalid log format" in issue for issue in issues)
    assert any(issue.startswith("[ERROR]") or issue.startswith("[CRITICAL]") for issue in issues)
