from string import hexdigits

from django.core.exceptions import ValidationError


def is_hex_validator(color):
    color = color.strip(' #')
    if not set(color).issubset(hexdigits):
        raise ValidationError(f'Код цвета не является шестнадцатеричным')
    if len(color) not in (3, 6):
        raise ValidationError(f'Код цвета имеет неправильную длину')
    return '#' + color
