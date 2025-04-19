from django.core.exceptions import ValidationError
import re


def validate_youtube_link(value):
    if not value:
        return
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    if not re.match(youtube_regex, value):
        raise ValidationError(
            'Ссылки на сторонние ресурсы запрещены. Разрешены только ссылки на YouTube (youtube.com или youtu.be).')
