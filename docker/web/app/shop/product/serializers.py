from django.db import IntegrityError
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, CharField, IntegerField, BooleanField, DecimalField

from assortment.models import Assortment
from assortment.serializers import AssortmentSerializer
from utils.response import get_error_message, C_API_EXCEPTION, C_PRICE_WRONG, C_QUANTITY_WRONG, C_USER_NOT_IN_COMPANY
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
            'id', 'name',
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


class ProductEntrySerializer(ModelSerializer):
    id = IntegerField(required=False)
    features = ProductFeatureSerializer(many=True, source='product_features')
    assortment = AssortmentSerializer(many=True, source='product_assortment', read_only=False)
    name = CharField(validators=[])

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'features', 'category', 'assortment',
        ]

    def validate_price(self, value):
        if self.context.get('action') == 'create' and int(value) == 0:
            raise ValidationError(get_error_message(C_PRICE_WRONG))
        return value

    def validate_quantity(self, value):
        if self.context.get('action') == 'create' and int(value) == 0:
            raise ValidationError(get_error_message(C_QUANTITY_WRONG))
        return value

    def validate(self, attrs):
        if not self.context.get('request').user.company:
            raise ValidationError(get_error_message(C_USER_NOT_IN_COMPANY))
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

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        instance.name = validated_data.get('name')
        instance.category = validated_data.get('category')
        instance.save()
        features = validated_data.get('product_features')
        assortments = validated_data.get('product_assortment')
        assortments = assortments[0]
        for item in features:
            feature, _ = Feature.objects.get_or_create(name=item.get('feature').get('name'))
            try:
                product_feature = ProductFeature.objects.get(
                    product=instance,
                    feature=feature,
                )
                product_feature.value = item.get('value')
                product_feature.save()
            except ProductFeature.DoesNotExist:
                product_feature = ProductFeature.objects.create(
                    product=instance,
                    feature=feature,
                    value=item.get('value'),
                )
                product_feature.save()
        try:
            assortment = Assortment.objects.get(
                company=user.company,
                product=instance
            )
            assortment.quantity = assortments.get('quantity')
            assortment.available = assortments.get('available')
            assortment.description = assortments.get('description')
            assortment.save()
        except Assortment.DoesNotExist:
            assortment = Assortment.objects.create(
                company=user.company,
                product=instance,
                quantity=assortments.get('quantity'),
                available=assortments.get('available'),
                description=assortments.get('description'),
            )
            assortment.save()

        return instance