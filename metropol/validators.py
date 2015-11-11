__author__ = 'Carlos'
import datetime

from django.core.exceptions import ValidationError


# Checks if the given date is a past date (not strictly)
def validate_past_date(date_to_validate):
    today = datetime.date.today()
    if date_to_validate > today:
        raise ValidationError('La fecha no puede ser en el futuro.')
