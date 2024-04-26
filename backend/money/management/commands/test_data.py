from django.core.management.base import BaseCommand

from core.factory import CollectFactory, PaymentFactory, UserFactory


class Command(BaseCommand):
    help = 'Создать тестовые данные'

    def handle(self, *args, **options):
        for _ in range(5):
            UserFactory.create()
        for _ in range(50):
            CollectFactory.create()
        for _ in range(2000):
            PaymentFactory.create()
