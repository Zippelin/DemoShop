import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.reverse import reverse

from profile.models import User


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
            (True, HTTP_200_OK),
            (None, HTTP_200_OK)
    )
)
@pytest.mark.django_db
def test_product_list(api_client, user_factory, product_factory, token_factory, is_authenticated, http_response):
    products = product_factory(_quantity=1)
    url = reverse('product-list')
    if is_authenticated:
        user = user_factory(user_type=User.Type.CUSTOMER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
            (True, HTTP_201_CREATED),
            (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_product_post(api_client, user_factory, category_factory, token_factory, company_factory, is_authenticated,
                      http_response):
    category = category_factory(_quantity=1)
    url = reverse('product-list')
    if is_authenticated:
        company = company_factory(_quantity=1)
        user = user_factory(user_type=User.Type.PROVIDER, company=company[0])
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "name": "string",
        "features": [
            {
                "feature": "string",
                "value": "string"
            }
        ],
        "category": category[0].id,
        "assortment": [
            {
                "price": 1,
                "description": "string",
                "quantity": 1,
                "available": True
            }
        ]
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
            (True, HTTP_200_OK),
            (None, HTTP_200_OK)
    )
)
@pytest.mark.django_db
def test_product_detail(api_client, user_factory, assortment_factory, token_factory, company_factory, is_authenticated,
                        http_response):
    assortments = assortment_factory(_quantity=1)
    url = reverse('product-detail', args=[assortments[0].product.id])
    if is_authenticated:
        company = company_factory(_quantity=1)
        user = user_factory(user_type=User.Type.PROVIDER, company=company[0])
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url)
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
            (True, HTTP_200_OK),
            (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_product_put(api_client, user_factory, assortment_factory, token_factory, company_factory, is_authenticated,
                     http_response):
    assortments = assortment_factory(_quantity=1)
    url = reverse('product-detail', args=[assortments[0].product.id])
    if is_authenticated:
        company = company_factory(_quantity=1)
        assortments[0].company = company[0]
        assortments[0].save()
        user = user_factory(user_type=User.Type.PROVIDER, company=company[0])
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "name": "string",
        "features": [
            {
                "feature": "string",
                "value": "string"
            }
        ],
        "category": assortments[0].product.category,
        "assortment": [
            {
                "price": 2,
                "description": "string",
                "quantity": 1,
                "available": True
            }
        ]
    }
    resp = api_client.put(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
            (True, HTTP_200_OK),
            (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_product_patch(api_client, user_factory, assortment_factory, token_factory, company_factory, is_authenticated,
                       http_response):
    assortments = assortment_factory(_quantity=1)
    url = reverse('product-detail', args=[assortments[0].product.id])
    if is_authenticated:
        company = company_factory(_quantity=1)
        assortments[0].company = company[0]
        assortments[0].save()
        user = user_factory(user_type=User.Type.PROVIDER, company=company[0])
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "name": "string",
        "features": [
            {
                "feature": "string",
                "value": "string"
            }
        ],
        "category": assortments[0].product.category,
        "assortment": [
            {
                "price": 3,
                "description": "string",
                "quantity": 1,
                "available": True
            }
        ]
    }
    resp = api_client.patch(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
            (True, HTTP_200_OK),
            (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_product_delete(api_client, user_factory, assortment_factory, token_factory, company_factory, is_authenticated,
                        http_response):
    assortments = assortment_factory(_quantity=1)
    url = reverse('product-detail', args=[assortments[0].id])
    if is_authenticated:
        user = user_factory(user_type=User.Type.PROVIDER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url, format='json')
    assert resp.status_code == http_response
