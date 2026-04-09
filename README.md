# Log Investigator

A Python-based log analysis tool for structured log files. It detects common issues such as invalid log format, missing fields, invalid IP addresses, invalid response times
, and server error status codes, then generates a clear text report.

## Features

- Parse structured log entries
- Detect common log issues
- Generate a readable report with summary
- Support CLI input/output arguments
- Include automated tests with `pytest`

## Project Structure

```text
log-investigato/
├── src/
│   └── log_investigator/
│       ├── __init__.py
│       ├── main.py
│       ├── log_parser.py
│       ├── log_analyzer.py
│       └── report_writer.py
├── tests/
├── sample_logs/
├── reports/
├── README.md
├── requirements.txt
└── .gitignore
Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Run

From the project root:

PYTHONPATH=src python3 -m log_investigator.main --input sample_logs/test.txt

Custom output file:

PYTHONPATH=src python3 -m log_investigator.main --input sample_logs/test.txt --output reports/custom_report.txt

LOG INVESTIGATION REPORT
Source file: sample_logs/test.txt
Total issues found: 8
Run Tests
PYTHONPATH=src pytest -q
