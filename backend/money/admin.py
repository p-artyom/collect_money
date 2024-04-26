from django.contrib import admin

from core.admin import BaseAdmin
from money.models import Collect, Payment
from money.utils import cut_string


@admin.register(Collect)
class CollectAdmin(BaseAdmin):
    list_display = (
        'pk',
        'author',
        'title',
        'reason',
        'short_description',
        'amount_money',
        'created',
        'modified',
        'deleted',
    )
    list_filter = ('reason',)
    search_fields = ('title',)

    def short_description(self, obj):
        return cut_string(obj.description)

    short_description.short_description = 'описание'


@admin.register(Payment)
class PaymentAdmin(BaseAdmin):
    list_display = (
        'pk',
        'author',
        'short_text',
        'amount',
        'collect',
        'created',
        'modified',
    )
    list_filter = ('created', 'modified')
    search_fields = ('author',)

    def short_text(self, obj):
        return cut_string(obj.text)

    short_text.short_description = 'текст сообщения'
