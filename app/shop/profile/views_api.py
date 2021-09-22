import allauth
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .permissions import UserIsProviderOrAdmin
from .models import Company
from product.models import Category, Feature, Product, ProductFeature
from assortment.models import Assortment
from utils.response import response, C_NO_INPUT_FILE, C_WRONG_FILE, C_WRONG_COMPANY_EMPLOYEE
import yaml


class ImportProductsView(APIView):
    permission_classes = [IsAuthenticated, UserIsProviderOrAdmin]

    def post(self, request, *args, **kwargs):
        if request.data.get('files'):
            try:
                loaded_data = yaml.safe_load(request.data.get('files'))
            except yaml.scanner.ScannerError:
                return response(
                    errors=C_WRONG_FILE
                )

            if request.user.is_superuser:
                return response(data=_create_record(loaded_data))
            else:
                company = Company.objects.filter(name=loaded_data['shop']).all()
                if len(company) == 1 and request.user.company == company[0]:
                    return response(data=_create_record(loaded_data))
                return response(errors=C_WRONG_COMPANY_EMPLOYEE)

        return response(errors=C_NO_INPUT_FILE)


def _create_record(loaded_data):
    company, _ = Company.objects.get_or_create(name=loaded_data['shop'])
    for category in loaded_data.get('categories'):
        new_cat, _ = Category.objects.get_or_create(**category)

    Assortment.objects.filter(company=company).all().delete()

    for item in loaded_data.get('goods'):

        product, _ = Product.objects.get_or_create(
            name=item['name'],
            category=Category.objects.get(id=item['category'])
        )

        Assortment.objects.create(
            company=company,
            product=product,
            price=item['price'],
            quantity=item['quantity'],
        )

        for feature_name, feature_value in item['parameters'].items():
            feature, _ = Feature.objects.get_or_create(name=feature_name)
            ProductFeature.objects.get_or_create(
                product=product,
                feature=feature,
                value=feature_value
            )
    return loaded_data


class ConfirmationSent(APIView):

    def get(self, request, *args, **kwargs):
        return JsonResponse({})