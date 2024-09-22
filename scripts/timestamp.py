#!/usr/bin/env python3
"""Script to convert unix timestamps to human readable format.

Auto-detects timestamp precision and handles accordingly.
Similar to unixtimestamp.com
"""

import argparse
from datetime import datetime, timezone


def _detect_timestamp_precision(timestamp: int) -> int:
    length = len(str(timestamp))
    if length == 10:
        return 1  # seconds
    if length == 13:
        return 1_000  # milliseconds
    if length == 16:
        return 1_000_000  # microseconds
    if length == 19:
        return 1_000_000_000  # nanoseconds
    raise ValueError("Invalid timestamp format")


def _normalize_timestamp(timestamp: int) -> float:
    precision = _detect_timestamp_precision(timestamp)
    timestamp_seconds = int(timestamp) / precision
    return timestamp_seconds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("timestamp", type=int)
    args = parser.parse_args()

    normalized = _normalize_timestamp(args.timestamp)
    utc_time = datetime.fromtimestamp(normalized, tz=timezone.utc)
    local_time = utc_time.astimezone()

    # Format as ISO 8601
    utc_iso = utc_time.isoformat()
    local_iso = local_time.isoformat()

    print(f"UTC time:   {utc_iso}")
    print(f"Local time: {local_iso}")


if __name__ == "__main__":
    main()
