import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.validators
import money.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Collect",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите заголовок",
                        max_length=200,
                        verbose_name="заголовок",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("Birthday", "День рождения"),
                            ("Happy Day", "День счастья"),
                            ("Goodness without a cause", "Добро без повода"),
                            ("Thinking of others", "Думаю о других"),
                            ("New good day", "Новый добрый день"),
                            ("Promotion", "Повышение"),
                            ("Taking advantage", "Пользуясь случаем"),
                            ("Just for fun", "Просто так"),
                            ("Birth of a child", "Рождение ребенка"),
                            ("Wedding", "Свадьба"),
                            ("Good habit", "Хорошая привычка"),
                        ],
                        help_text="Выберите повод",
                        max_length=200,
                        verbose_name="повод",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Введите описание",
                        max_length=2000,
                        verbose_name="описание",
                    ),
                ),
                (
                    "amount_money",
                    models.PositiveIntegerField(
                        help_text="Введите запланированную сумму. 0 - `бесконечный` сбор",
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(
                                100000000,
                            ),
                        ],
                        verbose_name="запланированная сумма",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Выберите обложку сбора",
                        null=True,
                        upload_to=money.models.collect_directory_path,
                        verbose_name="обложка сбора",
                    ),
                ),
                (
                    "deleted",
                    models.DateTimeField(
                        help_text="Введите дату и время завершения сбора",
                        validators=[core.validators.validate_datetime],
                        verbose_name="дата и время завершения сбора",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="Выберите автора",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "денежный сбор",
                "verbose_name_plural": "денежные сборы",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Введите текст сообщения",
                        max_length=2000,
                        verbose_name="текст сообщения",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Введите сумму",
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                        ],
                        verbose_name="сумма",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="Выберите автора",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="автор",
                    ),
                ),
                (
                    "collect",
                    models.ForeignKey(
                        help_text="Выберите денежный сбор",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="collects",
                        to="money.collect",
                        verbose_name="денежный сбор",
                    ),
                ),
            ],
            options={
                "verbose_name": "платёж для сбора",
                "verbose_name_plural": "платежи для сбора",
                "ordering": ("-created",),
            },
        ),
    ]
