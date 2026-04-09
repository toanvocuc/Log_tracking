import argparse
import sys
from pathlib import Path

from log_investigator.log_parser import read_log_file
from log_investigator.log_analyzer import analyze_logs
from log_investigator.report_writer import write_report


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="log-investigator",
        description="Analyze log files and generate an error report.",
        epilog="Example: PYTHONPATH=src python3 -m log_investigator.main --input sample_logs/test.txt"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input log file"
    )

    parser.add_argument(
        "--output",
        default="reports/report.txt",
        help="Path to the output report file (default: reports/report.txt)"
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    input_file = Path(args.input)
    output_file = Path(args.output)

    try:
        lines = read_log_file(input_file)
        issues = analyze_logs(lines)
        write_report(issues, output_file)

        print("Analysis complete. Report generated at: {}".format(output_file))
    except FileNotFoundError as error:
        print("Error: {}".format(error))
        sys.exit(1)


if __name__ == "__main__":
    main()
