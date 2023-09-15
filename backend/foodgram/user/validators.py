import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if not re.fullmatch(r"^[\w.@+-]+$", value):
        raise ValidationError("В username используются недопустимые символы")

    if value.lower() == "me":
        raise ValidationError("Укажите другой username")
