import re
from django.core.exceptions import ValidationError


def path_validator(path: str):
    if not re.match(pattern=r"^(/[a-zA-Z0-9_-]*)+$", string=path):
        raise ValidationError("Invalid UNIX formated path")


def color_validator(path: str):
    if not re.match(pattern=r"#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$", string=path):
        raise ValidationError("Invalid hexadecimal formated color")


def state_validator(state: str):
    states = ("active", "archived", "asleep")
    if state not in states:
        raise ValidationError("Invalid state")
