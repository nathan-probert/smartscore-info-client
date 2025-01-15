import datetime

import pytz


def get_date(hour=False, add_days=0, subtract_days=0):
    toronto_tz = pytz.timezone("America/Toronto")
    date = datetime.datetime.now(toronto_tz)
    if add_days:
        date += datetime.timedelta(days=add_days)
    if subtract_days:
        date -= datetime.timedelta(days=subtract_days)

    if hour:
        return date.strftime("%Y-%m-%dT%H:%M:%S")
    return date.strftime("%Y-%m-%d")


def find_difference_between_days(first, second):
    date1 = datetime.datetime.strptime(first, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(second, "%Y-%m-%d")
    return abs((date2 - date1).days)