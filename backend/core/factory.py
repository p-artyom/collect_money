import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from money.models import Collect, Payment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class CollectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collect

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

    text = factory.Faker('sentence')
    amount = factory.Faker('random_int')
