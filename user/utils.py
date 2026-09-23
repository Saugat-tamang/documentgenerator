from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def validate_user_password(password, user=None):
    try:
        validate_password(password, user)
    except ValidationError as e:
        return e.messages
    return None