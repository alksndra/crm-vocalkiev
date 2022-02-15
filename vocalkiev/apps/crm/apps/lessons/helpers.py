import datetime
from django.utils import timezone


def is_before_today(year, month, day):
    n = timezone.now()
    return datetime.datetime(n.year, n.month, n.day) > datetime.datetime(year, month, day)
