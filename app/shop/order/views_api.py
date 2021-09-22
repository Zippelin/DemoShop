from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from order.models import Order, OrderItem
from order.serializers import OrderItemSerializer, OrderListSerializer, OrderPatchSerializer, OrderRetrieveSerializer


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
        return Order.objects.filter(
            profile=self.request.user,
        ).all()

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}