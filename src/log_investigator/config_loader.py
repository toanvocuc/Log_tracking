import json
from pathlib import Path


DEFAULT_RULES = {
    "fail_status_codes": [500],
    "response_time_threshold_ms": 1000,
    "required_fields": ["Timestamp", "IP", "Status", "ResponseTime"],
    "fail_on_invalid_ip": True,
    "fail_on_invalid_format": True,
    "fail_on_missing_fields": True,
}


def load_rules(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError("Config file not found: {}".format(config_path))

    with config_path.open("r", encoding="utf-8") as file:
        loaded_rules = json.load(file)

    rules = DEFAULT_RULES.copy()
    rules.update(loaded_rules)

    return rules
