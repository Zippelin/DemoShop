from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from rest_framework.fields import IntegerField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer
from assortment.models import Assortment


class AssortmentSerializer(ModelSerializer):
    id = IntegerField(source='company.id', required=False)
    company = StringRelatedField()

    class Meta:
        model = Assortment
        fields = [
            'id', 'company', 'price', 'description', 'quantity', 'available'
        ]


class AssortmentShortSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    product = StringRelatedField()

    class Meta:
        model = Assortment
        fields = [
            'id', 'product'
        ]