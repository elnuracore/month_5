from rest_framework.exceptions import ValidationError
from datetime import date
from django.utils.timezone import now
from users.models import CustomUser

def validate_age(birth_date):
    if not birth_date:
        raise ValidationError("Show your birth_date to create a product")
    today = now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError("You must be at least 18 years old to create a product")
    return birth_date
