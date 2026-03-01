from django.core.exceptions import ValidationError


def forbidden_words(value: str):
    forbidden = ['bad', 'spam', 'xxx']
    for w in forbidden:
        if w in value.lower():
            raise ValidationError(f'Недопустимое слово в заголовке: {w}')