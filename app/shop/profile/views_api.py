from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .permissions import UserIsProviderOrAdmin
from .models import Company
from product.models import Category, Feature, Product, ProductFeature
from assortment.models import Assortment
import yaml


class ImportProductsView(APIView):
    permission_classes = [IsAuthenticated, UserIsProviderOrAdmin]

    def post(self, request, *args, **kwargs):
        if request.data.get('files'):
            try:
                loaded_data = yaml.safe_load(request.data.get('files'))
            except yaml.scanner.ScannerError:
                return JsonResponse({'message': "wrong file format"})

            if request.user.is_superuser:
                return JsonResponse({'message': "ok", 'data': _create_record(loaded_data)})
            else:
                company = Company.objects.filter(name=loaded_data['shop']).all()
                if len(company) == 1 and request.user.company == company:
                    return JsonResponse({'message': "ok", 'data': _create_record(loaded_data)})
                return JsonResponse({'message': "you must be employee for that company to import data"})

        return JsonResponse({'message': "need file for inport"})


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
            ProductFeature.objects.create(
                product=product,
                feature=feature,
                value=feature_value
            )
    return loaded_data
