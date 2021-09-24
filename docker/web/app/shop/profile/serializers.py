from rest_framework.serializers import ModelSerializer

from profile.models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name'
        ]