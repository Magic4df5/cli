import os
import pytest
from datetime import datetime, timezone
from log_analyzer.parser import parse_line, parse_timestamp
from log_analyzer.filter import filter_events
from log_analyzer.aggregation import aggregate_events
from log_analyzer.output import save_report
from log_analyzer.cli import process_file


def test_parse_timestamp_valid():
    dt = parse_timestamp("2026-09-01T00:08:59Z")
    assert dt.year == 2026
    assert dt.month == 9


def test_parse_timestamp_invalid():
    with pytest.raises(ValueError):
        parse_timestamp("2026-09-01 00:08:59")


def test_parse_line_valid():
    line = "2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created"
    res = parse_line(1, line)
    assert res["level"] == "WARN"
    assert res["source"] == "auth-api"
    assert res["event_code"] == "AUTH_LOGIN_OK"


def test_parse_line_invalid_fields():
    with pytest.raises(ValueError):
        parse_line(1, "invalid line content")


def test_parse_line_invalid_level():
    with pytest.raises(ValueError):
        parse_line(1, "2026-09-01T00:08:59Z | UNKNOWN | auth-api | CODE | msg")


def test_parse_line_empty():
    with pytest.raises(ValueError):
        parse_line(1, "   ")


def test_filter_events():
    dt1 = datetime(2026, 9, 1, 1, 0, tzinfo=timezone.utc)
    dt2 = datetime(2026, 9, 1, 3, 0, tzinfo=timezone.utc)
    events = [
        {"timestamp": dt1, "level": "INFO", "source": "api", "event_code": "OK"},
        {"timestamp": dt2, "level": "ERROR", "source": "db", "event_code": "ERR"}
    ]
    filtered = list(filter_events(events, start_from=dt1, end_to=dt2, level="INFO", source="api"))
    assert len(filtered) == 1


def test_aggregate_events():
    dt = datetime(2026, 9, 1, 1, 0, tzinfo=timezone.utc)
    events = [
        {"timestamp": dt, "level": "ERROR", "source": "db", "event_code": "ERR_DB"}
    ]
    summary = aggregate_events(events, 2, 1, [{"line": 2, "error": "err"}], top_n=1)
    assert summary["total_lines"] == 2
    assert summary["valid_lines"] == 1
    assert summary["error_lines_count"] == 1
    assert summary["top_error_codes"] == [("ERR_DB", 1)]


def test_empty_and_missing_files(tmp_path):
    empty_file = tmp_path / "empty.log"
    empty_file.write_text("", encoding="utf-8")
    events, errors, total, valid = process_file(str(empty_file))
    assert total == 0
    assert valid == 0


def test_json_csv_export(tmp_path):
    summary = {
        "total_lines": 10,
        "valid_lines": 8,
        "error_lines_count": 2,
        "error_lines_details": [{"line": 3, "error": "test"}],
        "filtered_count": 5,
        "levels_summary": {"INFO": 5},
        "sources_summary": {"api": 5},
        "top_error_codes": [("ERR", 1)]
    }
    json_path = tmp_path / "report.json"
    csv_path = tmp_path / "report.csv"

    save_report(summary, "json", str(json_path))
    save_report(summary, "csv", str(csv_path))

    assert json_path.exists()
    assert csv_path.exists()