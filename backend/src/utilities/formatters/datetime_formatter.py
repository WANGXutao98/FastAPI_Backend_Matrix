import time
from datetime import datetime, timedelta, timezone


def format_datetime_into_isoformat(date_time: datetime) -> str:
    iso_string_without_ms = date_time.replace(tzinfo=timezone(timedelta(hours=+8), "CST")).isoformat().split(".")[0]
    return iso_string_without_ms.replace("+08:00", "").replace("T", " ")


def format_datetime_into_timestamp(date_str: str) -> str:
    return int(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S"))) * 1000
