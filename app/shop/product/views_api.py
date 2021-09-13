from rest_framework.viewsets import ModelViewSet
from .models import Product, ProductFeature
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer