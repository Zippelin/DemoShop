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