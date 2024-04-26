import random

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.validators import REASONS
from money.models import Collect, Payment

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class CollectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collect

    author = User.objects.all()[random.randint(0, User.objects.count() - 1)]
    reason = random.choice(REASONS)[0]
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    amount_money = factory.Faker('random_int')
    deleted = factory.Faker(
        'date_time_this_month',
        before_now=False,
        after_now=True,
        tzinfo=timezone.get_current_timezone(),
    )


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    author = User.objects.all()[random.randint(0, User.objects.count() - 1)]
    text = random.choice(REASONS)[0]
    amount = factory.Faker('random_int')
    collect = Collect.objects.all()[
        random.randint(0, Collect.objects.count() - 1)
    ]
