from string import hexdigits

from django.core.exceptions import ValidationError


def is_hex_validator(color):
    color = color.strip(' #')
    if not set(color).issubset(hexdigits) and len(color) not in (3, 6):
        raise ValidationError(
            'Неправильный hex-код цвета'
        )
    return '#' + color
