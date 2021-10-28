from django.contrib import admin
from rest_framework.reverse import reverse_lazy

from order.models import OrderItem, Order

from utils.signals import new_order_confirmation


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['assortment', 'price', 'quantity', 'get_company']
    readonly_fields = ['assortment', 'price', 'get_company']

    def get_readonly_fields(self, request, obj=None):
        if obj.status == Order.Status.NEW:
            return ['assortment', 'price', 'get_company']
        return ['assortment', 'price', 'quantity', 'get_company']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    list_display = ['id', 'status', 'date', 'get_items_count', 'get_items_sum']

    def save_form(self, request, form, change):
        order = Order.objects.get(id=request.resolver_match.kwargs.get('object_id'))
        if order.status == Order.Status.NEW and request.POST.get('status') == Order.Status.IN_PROGRESS:
            new_order_confirmation.send(
                sender=self.__class__,
                order_number=order.id,
                order_url=reverse_lazy('order-detail', request=request, args=[order.id]),
                to_address=order.recipient_email,
                last_name=order.recipient_last_name,
                first_name=order.recipient_first_name,
            )
        return super(OrderAdmin, self).save_form(request, form, change)
