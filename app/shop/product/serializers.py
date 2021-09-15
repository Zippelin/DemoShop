from django.db import IntegrityError
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, CharField, IntegerField, BooleanField, DecimalField

from assortment.models import Assortment
from assortment.serializers import AssortmentSerializer
from utils.response import get_error_message, C_API_EXCEPTION
from .models import Product, ProductFeature, Feature, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name',
        ]


class FeatureSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = [
            'name',
        ]


class ProductFeatureSerializer(ModelSerializer):
    feature = CharField(source='feature.name')
    id = IntegerField(source='feature.id', required=False)

    class Meta:
        model = ProductFeature
        fields = [
            'id', 'feature', 'value'
        ]


class ProductListSerializer(ModelSerializer):
    category = StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category'
        ]


class ProductCommonSerializer(ModelSerializer):
    id = IntegerField(required=False)
    features = ProductFeatureSerializer(many=True, source='product_features')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'features', 'assortment'
        ]


class ProductEntrySerializer(ProductCommonSerializer):
    assortment = AssortmentSerializer(many=True, source='product_assortment', read_only=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'features', 'category', 'assortment',
        ]

    def validate_price(self, value):
        if self.context.get('action') == 'create' and int(value) == 0:
            raise ValidationError('Цена должна быть больше нуля')
        return value

    def validate_quantity(self, value):
        if self.context.get('action') == 'create' and int(value) == 0:
            raise ValidationError('Кол-во должно быть больше нуля')
        return value

    def validate(self, attrs):
        if not self.context.get('request').user.company:
            raise ValidationError('Пользователь должен состоять в организации')
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user

        features = validated_data.pop('product_features')
        assortment = validated_data.pop('product_assortment')
        assortment = assortment[0]

        try:
            product, _ = Product.objects.get_or_create(
                name=validated_data.get('name'),
                category=validated_data.get('category')
            )
        except IntegrityError:
            raise APIException(get_error_message(C_API_EXCEPTION))

        for item in features:
            try:
                feature, _ = Feature.objects.get_or_create(name=item.get('feature').get('name'))
                ProductFeature.objects.get_or_create(
                    product=product,
                    feature=feature,
                    value=item.get('value')
                )
            except IntegrityError:
                raise APIException(get_error_message(C_API_EXCEPTION))

        Assortment.objects.get_or_create(
            company=user.company,
            product=product,
            price=assortment['price'],
            quantity=assortment['quantity'],
            available=assortment['available'],
            description=assortment['description'],
        )

        return product
