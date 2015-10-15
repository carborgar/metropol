__author__ = 'Carlos'
from django.core.exceptions import ValidationError
import datetime


# Checks if the given date is a past date (not strictly)
def validate_past_date(date_to_validate):
    today = datetime.date.today()
    if date_to_validate > today:
        raise ValidationError('La fecha debe ser en el pasado.')
