from datetime import datetime as dt


def get_day_hour_from_timestamp(timestamp):
    if type(timestamp) == str:
        timestamp = dt.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    day = timestamp.day
    hour = timestamp.hour
    return day, hour

def get_datetime_from_timestamp(timestamp):
    return dt.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
