from collections import Counter


def aggregate_events(filtered_events, total_lines, valid_lines, error_lines, top_n=5):
    levels_summary = Counter()
    sources_summary = Counter()
    error_codes = Counter()

    filtered_count = 0
    for event in filtered_events:
        filtered_count += 1
        levels_summary[event["level"]] += 1
        sources_summary[event["source"]] += 1
        if event["level"] == "ERROR":
            error_codes[event["event_code"]] += 1

    top_errors = error_codes.most_common(top_n)

    return {
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "error_lines_count": len(error_lines),
        "error_lines_details": error_lines,
        "filtered_count": filtered_count,
        "levels_summary": dict(levels_summary),
        "sources_summary": dict(sources_summary),
        "top_error_codes": top_errors
    }