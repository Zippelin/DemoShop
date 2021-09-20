from abc import ABC

from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, DecimalField, EmailField, CharField, IntegerField
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from assortment.models import Assortment
from assortment.serializers import AssortmentShortSerializer
from order.models import OrderItem, Order
from product.models import Product
from utils.response import C_QUANTITY_WRONG, get_error_message, C_QUANTITY_THRESHOLD, C_WRONG_REQUEST


class OrderItemSerializer(ModelSerializer):
    id = IntegerField()
    price = SerializerMethodField()
    assortment = AssortmentShortSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'assortment', 'quantity', 'price'
        ]

    def get_price(self, obj):
        if obj.order.status == Order.Status.NEW:
            return obj.assortment.price
        return obj.price

    def validate_quantity(self, value):

        if self.context['action'] == 'create':
            try:
                assortment_id = self.context['request'].data.get('assortment').get('id')
            except:
                raise ValidationError(get_error_message(C_WRONG_REQUEST))

        try:
            if self.context['action'] == 'create':
                assortment = Assortment.objects.get(id=assortment_id)
            else:
                try:
                    order_id = self.context['request'].parser_context['kwargs']['pk']
                    assortment = OrderItem.objects.get(id=order_id).assortment
                except OrderItem.DoesNotExist:
                    raise ValidationError(get_error_message(C_WRONG_REQUEST))
        except Assortment.DoesNotExist:
            raise ValidationError(get_error_message(C_WRONG_REQUEST))

        if value < 1:
            raise ValidationError(get_error_message(C_QUANTITY_WRONG))
        elif value > assortment.quantity:
            raise ValidationError(get_error_message(C_QUANTITY_THRESHOLD))
        return value

    def create(self, validated_data):
        order, _ = Order.objects.get_or_create(
            status=Order.Status.NEW,
            profile=self.context['request'].user
        )
        try:
            assortment = Assortment.objects.get(id=validated_data['assortment'].get('id'))
        except Assortment.DoesNotExist:
            raise ValidationError(get_error_message(C_WRONG_REQUEST))
        order_item, is_created = OrderItem.objects.get_or_create(
            assortment=assortment,
            order=order
        )
        if not is_created:
            order_item.quantity += 1
            order_item.save()
            return order_item
        order_item = OrderItem.objects.create(
            assortment=assortment,
            quantity=validated_data['quantity'],
            price=assortment.product.price,
            order=order
        )
        order_item.save()
        return order_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data['quantity']
        instance.save()
        return instance


class OrderGenericSerializer(ModelSerializer):
    sum = SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'date', 'status',
            'recipient_email', 'recipient_first_name',
            'recipient_last_name',
            'recipient_patronymic', 'recipient_phone',
            'profile',
            'city', 'street', 'house_number', 'housing',
            'structure', 'apartment', 'additional_info',
            'sum'
        ]

    def get_sum(self, obj):
        total = 0
        for item in obj.order_items.all():
            total += item.quantity * item.price
        return total


class OrderListSerializer(OrderGenericSerializer):
    items_count = SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'date', 'status',
            'items_count', 'sum'
        ]

    def get_items_count(self, obj):
        obj.order_items.count()
        return obj.order_items.count()


class OrderRetrieveSerializer(OrderGenericSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'date', 'status',
            'recipient_email', 'recipient_first_name',
            'recipient_last_name',
            'recipient_patronymic', 'recipient_phone',
            'profile',
            'city', 'street', 'house_number', 'housing',
            'structure', 'apartment', 'additional_info',
            'order_items', 'sum'
        ]


class OrderPatchSerializer(OrderGenericSerializer):
    city = CharField(required=True)
    street = CharField(required=True)
    house_number = IntegerField(required=True)
    apartment = CharField(required=True)

    recipient_email = EmailField(required=True)
    recipient_first_name = CharField(required=True)
    recipient_last_name = CharField(required=True)
    recipient_patronymic = CharField(required=True)
    recipient_phone = CharField(required=True)

    def update(self, instance, validated_data):
        instance = super(OrderPatchSerializer, self).update(instance, validated_data)
        if validated_data['status'] == Order.Status.IN_PROGRESS \
                and instance.status == Order.Status.NEW:
            for order_item in instance.order_items.all():
                order_item.price = order_item.assortment.price
                order_item.save()
        return instance
