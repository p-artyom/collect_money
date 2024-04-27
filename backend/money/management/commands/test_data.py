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
        for _ in range(50):
            CollectFactory.create(
                author=User.objects.all()[
                    random.randint(0, User.objects.count() - 1)
                ],
                reason=random.choice(REASONS)[0],
            )
        for _ in range(2000):
            PaymentFactory.create(
                author=User.objects.all()[
                    random.randint(0, User.objects.count() - 1)
                ],
                collect=Collect.objects.all()[
                    random.randint(0, Collect.objects.count() - 1)
                ],
            )
