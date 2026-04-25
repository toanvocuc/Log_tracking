import argparse
import sys
from pathlib import Path

from log_investigator.config_loader import load_rules
from log_investigator.log_parser import read_log_file
from log_investigator.log_analyzer import analyze_logs
from log_investigator.report_writer import write_report


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="log-investigator",
        description="Analyze log files and generate an error report.",
        epilog=(
            "Example: PYTHONPATH=src python3 -m log_investigator.main "
            "--input sample_logs/test.txt --config config/rules.json"
        ),
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input log file",
    )

    parser.add_argument(
        "--output",
        default="reports/report.txt",
        help="Path to the output report file (default: reports/report.txt)",
    )

    parser.add_argument(
        "--config",
        default="config/rules.json",
        help="Path to the rules config file (default: config/rules.json)",
    )

    parser.add_argument(
        "--fail-on-any-issue",
        action="store_true",
        help="Exit with code 1 if at least one issue is found",
    )

    parser.add_argument(
        "--max-issues",
        type=int,
        default=None,
        help="Exit with code 1 if the number of issues is greater than this value",
    )

    return parser.parse_args()


def determine_exit_code(issue_count: int, fail_on_any_issue: bool, max_issues):
    if fail_on_any_issue and issue_count > 0:
        return 1

    if max_issues is not None and issue_count > max_issues:
        return 1

    return 0


def main() -> None:
    args = parse_arguments()

    input_file = Path(args.input)
    output_file = Path(args.output)
    config_file = Path(args.config)

    try:
        rules = load_rules(config_file)
        lines = read_log_file(input_file)
        issues = analyze_logs(lines, rules)
        write_report(issues, output_file, input_file)

        print("Analysis complete. Report generated at: {}".format(output_file))
        print("Config file used: {}".format(config_file))
        print("Total issues found: {}".format(len(issues)))

        exit_code = determine_exit_code(
            issue_count=len(issues),
            fail_on_any_issue=args.fail_on_any_issue,
            max_issues=args.max_issues,
        )

        sys.exit(exit_code)

    except FileNotFoundError as error:
        print("Error: {}".format(error))
        sys.exit(2)


if __name__ == "__main__":
    main()
