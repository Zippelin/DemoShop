from rest_framework.viewsets import ModelViewSet
from .models import Product
from rest_framework.permissions import IsAuthenticated
from profile.permissions import UserIsProviderOrAdmin
from .serializers import ProductListSerializer, ProductEntrySerializer


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'destroy', 'update', 'partial_update',]:
            self.serializer_class = ProductEntrySerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update', ]:
            return [IsAuthenticated(), UserIsProviderOrAdmin()]
        return []

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}