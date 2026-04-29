# Containerized Demo App with Log Quality Gate

A small DevOps-focused project that combines a containerized FastAPI demo application with a custom Python log analysis tool.

The demo application generates realistic logs through normal, slow, and error endpoints. The log quality gate reads those logs, applies configurable rules, generates a report, and can return exit codes based on detected issues.

## Project Goals

- Build a small web application that produces realistic logs
- Containerize the application with Docker
- Analyze generated logs using a custom Python tool
- Apply configurable validation rules to log data
- Produce readable reports for troubleshooting and automation

## Current Features

### Demo App
- FastAPI-based demo service
- `/health` endpoint for normal requests
- `/slow` endpoint for slow responses
- `/error` endpoint for simulated server errors
- Structured log output written to file

### Log Quality Gate
- Parse structured log lines
- Detect common issues such as:
  - Invalid log format
  - Missing required fields
  - Invalid IP addresses
  - Invalid response times
  - Server error status codes
  - High response times above threshold
- Load validation rules from a JSON config file
- Generate text reports with:
  - source file
  - total issue count
  - summary by severity
  - summary by issue type
  - detailed issue list
- Return exit codes for automation and pipeline usage

## Project Structure

```text
log-investigato/
├── config/
│   └── rules.json
├── demo_app/
│   ├── app/
│   │   └── main.py
│   ├── logs/
│   │   └── app.log
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
├── reports/
│   ├── report.txt
│   └── demo_app_report.txt
├── src/
│   └── log_investigator/
│       ├── __init__.py
│       ├── config_loader.py
│       ├── log_analyzer.py
│       ├── log_parser.py
│       ├── main.py
│       ├── models.py
│       └── report_writer.py
├── tests/
│   ├── test_log_analyzer.py
│   ├── test_log_parser.py
│   └── test_report_writer.py
├── README.md
├── requirements.txt
└── pyproject.toml
