import argparse
import sys
from datetime import datetime
from log_analyzer.parser import parse_line
from log_analyzer.filter import filter_events
from log_analyzer.aggregation import aggregate_events
from log_analyzer.output import print_summary, save_report


def process_file(file_path):
    valid_events = []
    error_lines = []
    total_lines = 0
    valid_lines = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                total_lines += 1
                try:
                    event = parse_line(line_num, line)
                    valid_events.append(event)
                    valid_lines += 1
                except Exception as e:
                    error_lines.append({"line": line_num, "error": str(e)})
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    return valid_events, error_lines, total_lines, valid_lines


def main():
    parser = argparse.ArgumentParser(description="Log Analyzer CLI")
    parser.add_argument("--input", required=True, help="Path to log file")
    parser.add_argument("--from", dest="from_time", help="Start timestamp ISO 8601 (inclusive)")
    parser.add_argument("--to", dest="to_time", help="End timestamp ISO 8601 (exclusive)")
    parser.add_argument("--level", help="Log level filter")
    parser.add_argument("--source", help="Source component filter")
    parser.add_argument("--top", type=int, default=5, help="Top N error codes")
    parser.add_argument("--format", choices=["json", "csv"], help="Export format")
    parser.add_argument("--output", help="Output file path for export")

    args = parser.parse_args()

    start_from = datetime.fromisoformat(args.from_time.replace("Z", "+00:00")) if args.from_time else None
    end_to = datetime.fromisoformat(args.to_time.replace("Z", "+00:00")) if args.to_time else None

    valid_events, error_lines, total_lines, valid_lines = process_file(args.input)
    filtered = filter_events(valid_events, start_from, end_to, args.level, args.source)
    summary = aggregate_events(filtered, total_lines, valid_lines, error_lines, args.top)

    print_summary(summary)

    if args.format and args.output:
        save_report(summary, args.format, args.output)
        print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()