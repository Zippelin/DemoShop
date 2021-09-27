from rest_framework.exceptions import APIException
from rest_framework.viewsets import ModelViewSet
from .models import Product, Feature
from rest_framework.permissions import IsAuthenticated
from profile.permissions import UserIsProviderOrAdmin
from .serializers import ProductListSerializer, ProductEntrySerializer, FeatureSerializer
from assortment.models import Assortment

from utils.response import get_error_message, C_API_EXCEPTION

from utils.response import response


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'destroy', 'update', 'partial_update', ]:
            self.serializer_class = ProductEntrySerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update', ]:
            return [IsAuthenticated(), UserIsProviderOrAdmin()]
        return []

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

    def destroy(self, request, *args, **kwargs):
        assortment_id = request.parser_context.get('kwargs').get('pk')
        try:
            assortment = Assortment.objects.get(id=assortment_id)
            assortment.delete()
            return response(data={'id': str(assortment_id)})
        except Assortment.DoesNotExist:
            raise APIException(get_error_message(C_API_EXCEPTION))


class FeatureAPIView(ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update', ]:
            return [IsAuthenticated(), UserIsProviderOrAdmin()]
        return [IsAuthenticated()]
