from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import TimestampedModel
from core.validators import REASONS, validate_datetime
from money.utils import cut_string

User = get_user_model()


def collect_directory_path(instance, filename):
    return f'collect/{instance.author}/{filename}'


class Collect(TimestampedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        help_text='Выберите автора',
    )
    title = models.CharField(
        'заголовок',
        max_length=200,
        help_text='Введите заголовок',
    )
    reason = models.CharField(
        'повод',
        max_length=200,
        choices=REASONS,
        help_text='Выберите повод',
    )
    description = models.TextField(
        'описание',
        max_length=2000,
        help_text='Введите описание',
    )
    amount_money = models.PositiveIntegerField(
        'запланированная сумма',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100000000),
        ],
        help_text='Введите запланированную сумму. 0 - `бесконечный` сбор',
    )
    image = models.ImageField(
        'обложка сбора',
        upload_to=collect_directory_path,
        blank=True,
        null=True,
        help_text='Выберите обложку сбора',
    )
    deleted = models.DateTimeField(
        'дата и время завершения сбора',
        help_text='Введите дату и время завершения сбора',
        validators=[
            validate_datetime,
        ],
    )

    class Meta:
        verbose_name = 'денежный сбор'
        verbose_name_plural = 'денежные сборы'
        ordering = ('-created',)

    def __str__(self) -> str:
        return cut_string(self.title)


class Payment(TimestampedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        help_text='Выберите автора',
    )
    text = models.TextField(
        'текст сообщения',
        max_length=2000,
        help_text='Введите текст сообщения',
    )
    amount = models.DecimalField(
        'сумма',
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
        ],
        help_text='Введите сумму',
    )
    collect = models.ForeignKey(
        Collect,
        on_delete=models.PROTECT,
        related_name='collects',
        verbose_name='денежный сбор',
        help_text='Выберите денежный сбор',
    )

    class Meta:
        verbose_name = 'платёж для сбора'
        verbose_name_plural = 'платежи для сбора'
        ordering = ('-created',)

    def __str__(self) -> str:
        return f'{self.author} отправил донат на {self.collect}'
