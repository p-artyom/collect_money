from django.core.exceptions import ValidationError
from django.utils import timezone

REASONS = (
    ('Birthday', 'День рождения'),
    ('Happy Day', 'День счастья'),
    ('Goodness without a cause', 'Добро без повода'),
    ('Thinking of others', 'Думаю о других'),
    ('New good day', 'Новый добрый день'),
    ('Promotion', 'Повышение'),
    ('Taking advantage', 'Пользуясь случаем'),
    ('Just for fun', 'Просто так'),
    ('Birth of a child', 'Рождение ребенка'),
    ('Wedding', 'Свадьба'),
    ('Good habit', 'Хорошая привычка'),
)


def validate_datetime(value):
    if value < timezone.now():
        raise ValidationError(
            'Дата и время завершения сбора не может быть меньше '
            'текущих даты и времени!',
        )
    return value
