from datetime import datetime

VALID_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "ERROR"}


def parse_timestamp(ts_str):
    ts_str = ts_str.strip()
    if not ts_str.endswith("Z") and "+" not in ts_str and "-" not in ts_str[10:]:
        raise ValueError("timestamp lacks ISO 8601 timezone")
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))


def parse_line(line_num, line):
    line = line.rstrip("\r\n")
    if not line.strip():
        raise ValueError("empty line")

    parts = line.split(" | ")
    if len(parts) != 5:
        parts = [p.strip() for p in line.split(" |", 4)]
        if len(parts) != 5:
            raise ValueError("invalid field count")

    ts_str, level, source, event_code, message = parts

    timestamp = parse_timestamp(ts_str)

    level = level.strip()
    if level not in VALID_LEVELS:
        raise ValueError(f"invalid level: {level}")

    source = source.strip()
    if not source:
        raise ValueError("empty source")

    event_code = event_code.strip()
    if not event_code:
        raise ValueError("missing event code")

    message = message.strip()

    return {
        "line_number": line_num,
        "timestamp": timestamp,
        "level": level,
        "source": source,
        "event_code": event_code,
        "message": message
    }