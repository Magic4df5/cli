def filter_events(events, start_from=None, end_to=None, level=None, source=None):
    for event in events:
        if start_from and event["timestamp"] < start_from:
            continue
        if end_to and event["timestamp"] >= end_to:
            continue
        if level and event["level"] != level.upper():
            continue
        if source and event["source"] != source:
            continue
        yield event