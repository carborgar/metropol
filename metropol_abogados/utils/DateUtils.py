__author__ = 'Carlos'
from datetime import datetime


def convert_date_to_datetime(date_to_convert):
    return datetime.combine(date_to_convert, datetime.min.time())