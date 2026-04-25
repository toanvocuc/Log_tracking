from typing import List
import ipaddress

from log_investigator.log_parser import parse_log_line


def is_valid_ip(ip_value: str) -> bool:
    try:
        ipaddress.ip_address(ip_value)
        return True
    except ValueError:
        return False


def is_valid_response_time(response_time: str) -> bool:
    if not response_time.endswith("ms"):
        return False

    number_part = response_time[:-2]
    return number_part.isdigit()


def response_time_to_int(response_time: str) -> int:
    return int(response_time[:-2])


def analyze_logs(lines: List[str], rules: dict) -> List[str]:
    issues = []

    required_fields = rules["required_fields"]
    fail_status_codes = [str(code) for code in rules["fail_status_codes"]]
    response_time_threshold_ms = rules["response_time_threshold_ms"]
    fail_on_invalid_ip = rules["fail_on_invalid_ip"]
    fail_on_invalid_format = rules["fail_on_invalid_format"]
    fail_on_missing_fields = rules["fail_on_missing_fields"]

    for line_number, line in enumerate(lines, start=1):
        parsed = parse_log_line(line)

        if parsed is None:
            if fail_on_invalid_format:
                issues.append("Line {}: Invalid log format -> {}".format(line_number, line))
            continue

        missing_fields = [field for field in required_fields if field not in parsed]

        if missing_fields:
            if fail_on_missing_fields:
                issues.append(
                    "Line {}: Missing field(s): {} -> {}".format(
                        line_number, ", ".join(missing_fields), line
                    )
                )
            continue

        if fail_on_invalid_ip and not is_valid_ip(parsed["IP"]):
            issues.append("Line {}: Invalid IP address -> {}".format(line_number, parsed["IP"]))

        if parsed["Status"] in fail_status_codes:
            issues.append(
                "Line {}: Server error status detected -> {}".format(line_number, parsed["Status"])
            )

        if not is_valid_response_time(parsed["ResponseTime"]):
            issues.append(
                "Line {}: Invalid response time -> {}".format(line_number, parsed["ResponseTime"])
            )
        else:
            response_time_ms = response_time_to_int(parsed["ResponseTime"])
            if response_time_ms > response_time_threshold_ms:
                issues.append(
                    "Line {}: High response time -> {} (threshold: {}ms)".format(
                        line_number, parsed["ResponseTime"], response_time_threshold_ms
                    )
                )

    return issues
