from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from api.permissions import AuthorCanEditAndDelete
from api.serializers import (
    CollectListSerializer,
    CollectRetrieveSerializer,
    CollectSerializer,
    PaymentSerializer,
)
from core.paginations import Pagination
from money.models import Collect, Payment
from money.tasks import send_message_user


@extend_schema_view(
    list=extend_schema(
        summary='Получить список групповых сборов',
        description=('Возвращает список групповых сборов.'),
    ),
    create=extend_schema(
        summary='Создать групповой сбор',
        description=('Создаёт групповой сбор.'),
    ),
    retrieve=extend_schema(
        summary='Получить данные конкретного группового сбора',
        description=('Возвращает данные конкретного группового сбора.'),
    ),
    update=extend_schema(
        summary='Обновить данные группового сбора целиком',
        description=('Обновить данные группового сбора целиком.'),
    ),
    partial_update=extend_schema(
        summary='Обновить данные группового сбора частично',
        description=('Обновить данные группового сбора частично.'),
    ),
    destroy=extend_schema(
        summary='Удалить групповой сбор',
        description=('Удалить групповой сбор.'),
    ),
)
class CollectViewSet(ModelViewSet):
    '''Групповой денежный сбор.'''

    pagination_class = Pagination
    permission_classes = (AuthorCanEditAndDelete,)
    queryset = Collect.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        send_message_user.delay(
            'Cоздание сбора',
            'Ваш групповой сбор успешно создан!',
            self.request.user.email,
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return CollectListSerializer
        if self.action == 'retrieve':
            return CollectRetrieveSerializer
        return CollectSerializer

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super(CollectViewSet, self).dispatch(*args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary='Получить список платежей',
        description=('Возвращает список платежей.'),
    ),
    create=extend_schema(
        summary='Создать платёж',
        description=('Создаёт платёж.'),
    ),
    retrieve=extend_schema(
        summary='Получить данные конкретного платежа',
        description=('Возвращает данные конкретного платежа.'),
    ),
    update=extend_schema(
        summary='Обновить данные платежа целиком',
        description=('Обновить данные платежа целиком.'),
    ),
    partial_update=extend_schema(
        summary='Обновить данные платежа частично',
        description=('Обновить данные платежа частично.'),
    ),
    destroy=extend_schema(
        summary='Удалить платёж',
        description=('Удалить платёж.'),
    ),
)
class PaymentViewSet(ModelViewSet):
    '''Платёж для сбора.'''

    serializer_class = PaymentSerializer
    pagination_class = Pagination
    permission_classes = (AuthorCanEditAndDelete,)

    def get_queryset(self):
        return Payment.objects.filter(
            collect=get_object_or_404(
                Collect,
                pk=self.kwargs.get('collect_id'),
            ),
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            collect=get_object_or_404(
                Collect,
                id=self.kwargs.get('collect_id'),
            ),
        )
        send_message_user.delay(
            'Отправка платежа',
            'Ваш платежа успешно отправлен!',
            self.request.user.email,
        )

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super(PaymentViewSet, self).dispatch(*args, **kwargs)
