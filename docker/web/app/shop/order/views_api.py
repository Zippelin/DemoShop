from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, extend_schema_serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from order.models import Order, OrderItem
from order.serializers import OrderItemSerializer, OrderListSerializer, OrderPatchSerializer, OrderRetrieveSerializer

from utils.response import response, C_METHOD_NOT_ALLOWED


@extend_schema_view(
    list=extend_schema(description='Список позиций заказа авторизированного пользователя.<br>'
                                   'Список содержит элементы из конзины.'),
    retrieve=extend_schema(description='Получение элемента заказа.'),
    update=extend_schema(description='Перезапись элемента заказа.'),
    partial_update=extend_schema(description='Обновление элемента заказа.'),
    destroy=extend_schema(description='Удаление элемента заказа.'),
    create=extend_schema(description='Добавление элемента заказа.<br>'
                                     'Если это первый элемент корзины, то создает заказ с статусом NEW'),
)
class OrderItemAPI(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__profile=self.request.user,
            order__status=Order.Status.NEW
        ).all()

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


@extend_schema_view(
    list=extend_schema(description='Список заказов авторизованного пользователя. Не являющихся корзиной.'),
    retrieve=extend_schema(
        description='Заказ авторизованного пользователя.',
        request=OrderRetrieveSerializer,
        responses=OrderRetrieveSerializer,
                           ),
    update=extend_schema(
        description='Перезапись заказа авторизованного пользователя.',
        request=OrderPatchSerializer,
        responses=OrderPatchSerializer,
                         ),
    partial_update=extend_schema(
        description='Обновление заказа авторизованного пользователя.',
        request=OrderPatchSerializer,
        responses=OrderPatchSerializer,
                                 ),
    destroy=extend_schema(description='Удаление заказа авторизованного пользователя.'),
    create=extend_schema(description='Создание заказа авторизованного пользователя.'),
)
class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', ]:
            self.serializer_class = OrderPatchSerializer
        elif self.action in ['retrieve', ]:
            self.serializer_class = OrderRetrieveSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action in ['update', 'partial_update', ]:
            return Order.objects.filter(
                Q(profile=self.request.user) &
                ~Q(status=Order.Status.DONE) & ~Q(status=Order.Status.CANCELED)
            ).all()
        else:
            return Order.objects.filter(
                Q(profile=self.request.user) &
                ~Q(status=Order.Status.NEW)
            ).all()

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}