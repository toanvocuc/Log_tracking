from pathlib import Path

from log_investigator.log_parser import read_log_file
from log_investigator.log_analyzer import analyze_logs
from log_investigator.report_writer import write_report

def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    input_file = project_root / "sample_logs" / "test.txt"
    output_file = project_root / "reports" / "report.txt"

    lines = read_log_file(input_file)
    issues = analyze_logs(lines)
    write_report(issues, output_file)

    print("Analysis complete. Report generated at: {}".format(output_file))


if __name__ == "__main__":
    main()
