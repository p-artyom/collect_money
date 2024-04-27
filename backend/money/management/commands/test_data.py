import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.factory import CollectFactory, PaymentFactory, UserFactory
from core.validators import REASONS
from money.models import Collect


class Command(BaseCommand):
    help = 'Создать тестовые данные'

    def handle(self, *args, **options):
        User = get_user_model()

        for _ in range(5):
            UserFactory.create()
        authors_data = User.objects.all()
        for _ in range(50):
            CollectFactory.create(
                author=random.choice(authors_data),
                reason=random.choice(REASONS)[0],
            )
        collects_data = Collect.objects.all()
        for _ in range(2000):
            PaymentFactory.create(
                author=random.choice(authors_data),
                collect=random.choice(collects_data),
            )
