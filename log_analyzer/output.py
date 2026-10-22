import json
import csv


def print_summary(summary):
    print("Log Analysis Summary")
    print(f"Total lines processed: {summary['total_lines']}")
    print(f"Valid records: {summary['valid_lines']}")
    print(f"Erroneous records: {summary['error_lines_count']}")
    if summary['error_lines_details']:
        print("Errors encountered:")
        for err in summary['error_lines_details']:
            print(f"  Line {err['line']}: {err['error']}")
    print(f"Filtered events count: {summary['filtered_count']}")

    print("\nSummary by Level:")
    for lvl, count in summary['levels_summary'].items():
        print(f"  {lvl}: {count}")

    print("\nSummary by Source:")
    for src, count in summary['sources_summary'].items():
        print(f"  {src}: {count}")

    print("\nTop Error Codes:")
    for code, count in summary['top_error_codes']:
        print(f"  {code}: {count}")


def save_report(summary, format_type, output_path):
    if format_type.lower() == 'json':
        serializable_summary = summary.copy()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_summary, f, indent=2, ensure_ascii=False)
    elif format_type.lower() == 'csv':
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["total_lines", summary["total_lines"]])
            writer.writerow(["valid_lines", summary["valid_lines"]])
            writer.writerow(["error_lines_count", summary["error_lines_count"]])
            writer.writerow(["filtered_count", summary["filtered_count"]])
            writer.writerow([])
            writer.writerow(["Level", "Count"])
            for lvl, count in summary["levels_summary"].items():
                writer.writerow([lvl, count])
            writer.writerow([])
            writer.writerow(["Source", "Count"])
            for src, count in summary["sources_summary"].items():
                writer.writerow([src, count])
            writer.writerow([])
            writer.writerow(["Error Code", "Count"])
            for code, count in summary["top_error_codes"]:
                writer.writerow([code, count])