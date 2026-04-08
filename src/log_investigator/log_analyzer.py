from typing import List
import ipaddress

from log_investigator.log_parser import parse_log_line


def is_valid_ip(ip_value: str) -> bool:
    """
    Check whether the IP address is valid.
    """
    try:
        ipaddress.ip_address(ip_value)
        return True
    except ValueError:
        return False


def is_valid_response_time(response_time: str) -> bool:
    """
    Check whether response time looks like '50ms' or '1200ms'.
    """
    if not response_time.endswith("ms"):
        return False

    number_part = response_time[:-2]
    return number_part.isdigit()


def analyze_logs(lines: List[str]) -> List[str]:
    """
    Analyze all log lines and return a list of detected issues.
    """
    issues = []

    for line_number, line in enumerate(lines, start=1):
        parsed = parse_log_line(line)

        if parsed is None:
            issues.append("Line {}: Invalid log format -> {}".format(line_number, line))
            continue

        required_fields = ["Timestamp", "IP", "Status", "ResponseTime"]
        missing_fields = [field for field in required_fields if field not in parsed]

        if missing_fields:
            issues.append(
                "Line {}: Missing field(s): {} -> {}".format(
                    line_number,
                    ", ".join(missing_fields),
                    line
                )
            )
            continue

        if not is_valid_ip(parsed["IP"]):
            issues.append(
                "Line {}: Invalid IP address -> {}".format(line_number, parsed["IP"])
            )

        if parsed["Status"] == "500":
            issues.append(
                "Line {}: Server error status detected -> {}".format(
                    line_number, parsed["Status"]
                )
            )

        if not is_valid_response_time(parsed["ResponseTime"]):
            issues.append(
                "Line {}: Invalid response time -> {}".format(
                    line_number, parsed["ResponseTime"]
                )
            )

    return issues
