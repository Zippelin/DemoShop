import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from profile.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category_factory():
    def factory(**kwargs):
        return baker.make('product.Category', make_m2m=True, **kwargs)
    return factory


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('product.Product', make_m2m=True, **kwargs)
    return factory


@pytest.fixture
def assortment_factory():
    def factory(**kwargs):
        return baker.make('assortment.Assortment', make_m2m=True, **kwargs)
    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('order.Order', **kwargs)
    return factory


@pytest.fixture
def feature_factory():
    def factory(**kwargs):
        return baker.make('product.Feature', make_m2m=True, **kwargs)
    return factory


@pytest.fixture
def order_item_factory():
    def factory(**kwargs):
        return baker.make('order.OrderItem', make_m2m=True, **kwargs)
    return factory


@pytest.fixture
def user_factory():
    def factory(**kwargs):
        return get_user_model().objects.create(
            username="user",
            password="user",
            email="user@user.com",
            type=kwargs['user_type'],
            company=kwargs.get('company', None)
        )
    return factory


@pytest.fixture
def company_factory():
    def factory(**kwargs):
        return baker.make('profile.Company', **kwargs)
    return factory


@pytest.fixture
def token_factory():
    def factory(**kwargs):
        if kwargs['user'].is_active:
            return Token.objects.create(user=kwargs['user']).key
        else:
            return ''
    return factory