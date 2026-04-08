from log_investigator.log_parser import parse_log_line


def test_parse_valid_log_line():
    line = "Timestamp:12:01|IP:10.0.0.1|Status:500|ResponseTime:1200ms"

    result = parse_log_line(line)

    assert result is not None
    assert result["Timestamp"] == "12:01"
    assert result["IP"] == "10.0.0.1"
    assert result["Status"] == "500"
    assert result["ResponseTime"] == "1200ms"


def test_parse_invalid_log_line():
    line = "random text not valid"

    result = parse_log_line(line)

    assert result is None
