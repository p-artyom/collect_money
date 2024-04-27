from django.contrib.auth import get_user_model
from django.db.models import Sum
from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.fields import Base64ImageField
from money.models import Collect, Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
        )


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'author',
            'text',
            'amount',
            'collect',
            'created',
            'modified',
        )
        read_only_fields = (
            'author',
            'created',
            'modified',
        )


class PaymentShortSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'amount',
            'created',
            'author',
            'text',
        )


class CollectSerializer(ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'reason',
            'description',
            'amount_money',
            'image',
            'created',
            'modified',
            'deleted',
        )
        read_only_fields = (
            'author',
            'created',
            'modified',
        )


class CollectListSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'reason',
            'amount_money',
            'deleted',
        )


class CollectRetrieveSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False)
    today_money = SerializerMethodField()
    donate_count = SerializerMethodField()
    list_collect = SerializerMethodField()

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'title',
            'reason',
            'description',
            'amount_money',
            'today_money',
            'donate_count',
            'list_collect',
            'image',
            'created',
            'modified',
            'deleted',
        )

    @extend_schema_field({'type': 'decimal.Decimal', 'example': 287647.47})
    def get_today_money(self, object):
        return object.collects.aggregate(Sum('amount'))['amount__sum']

    @extend_schema_field({'type': 'int', 'example': 3})
    def get_donate_count(self, object):
        return object.collects.all().count()

    @extend_schema_field(PaymentShortSerializer)
    def get_list_collect(self, object):
        return PaymentShortSerializer(
            object.collects.all(),
            many=True,
        ).data
