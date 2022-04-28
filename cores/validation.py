import re

from django.core.exceptions import ValidationError

from django.http  import JsonResponse

def email_validate(email):
    REGEXR_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(REGEXR_EMAIL, email) == None:
        raise ValidationError("INVALID_EMAIL")

def password_validate(password):
    REGEXR_PASSWORD = '^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[$@$!%*#?&])[A-Za-z0-9$@$!%*#?&].{8,}$'
    if re.match(REGEXR_PASSWORD, password) == None:
        raise ValidationError ("INVALID_PASSWORD")