from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from profile.models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name'
        ]


class ImportResponseSerializer(Serializer):
    detail = CharField()
    status = CharField()