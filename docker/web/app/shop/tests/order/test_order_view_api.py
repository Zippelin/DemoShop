import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.reverse import reverse

from order.models import Order
from profile.models import User


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_list(api_client, user_factory, order_factory, token_factory, is_authenticated, http_response):
    url = reverse('order-list')
    if is_authenticated:
        user = user_factory(user_type=User.Type.CUSTOMER)
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
def test_order_patch(api_client, user_factory, token_factory, order_factory, is_authenticated, http_response):
    orders = order_factory(_quantity=1)
    orders[0].status = Order.Status.IN_PROGRESS
    url = reverse('order-detail', args=[orders[0].id])
    if is_authenticated:
        token = token_factory(user=orders[0].profile)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "recipient_first_name": "firstName",
        "recipient_last_name": "lastName",
    }
    resp = api_client.patch(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_201_CREATED),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_post(api_client, user_factory, token_factory, order_factory, is_authenticated, http_response):
    orders = order_factory(_quantity=1)
    url = reverse('order-list')
    if is_authenticated:
        token = token_factory(user=orders[0].profile)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "status": "IN_PROGRESS",
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_items_list(api_client, user_factory, token_factory, order_item_factory, is_authenticated, http_response):
    order_items = order_item_factory(_quantity=1)
    url = reverse('orderitem-list')
    if is_authenticated:
        user = order_items[0].order.profile
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_items_list(api_client, user_factory, token_factory, order_item_factory, is_authenticated, http_response):
    order_items = order_item_factory(_quantity=1)
    url = reverse('orderitem-list')
    if is_authenticated:
        user = order_items[0].order.profile
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url, format='json')
    assert resp.status_code == http_response
    order_items[0].order.status = Order.Status.IN_PROGRESS
    order_items[0].order.save()
    resp = api_client.get(url, format='json')
    if is_authenticated:
        assert 0 == len(resp.json())


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_201_CREATED),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_items_post(api_client, user_factory, token_factory, assortment_factory, is_authenticated, http_response):
    assortment = assortment_factory(_quantity=1)
    url = reverse('orderitem-list')
    if is_authenticated:
        user = user_factory(user_type=User.Type.CUSTOMER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        'assortment': {
            'id': assortment[0].id
        },
        'quantity': 1
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_items_detail(api_client, token_factory, order_item_factory, is_authenticated, http_response):
    order_items = order_item_factory(_quantity=1)
    order_items[0].order.status = Order.Status.NEW
    order_items[0].order.save()
    url = reverse('orderitem-detail', args=[order_items[0].id])
    if is_authenticated:
        user = order_items[0].order.profile
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_items_put(api_client, token_factory, order_item_factory, assortment_factory, is_authenticated, http_response):
    assortment = assortment_factory(_quantity=1)
    order_items = order_item_factory(_quantity=1)
    order_items[0].order.status = Order.Status.NEW
    order_items[0].order.save()
    url = reverse('orderitem-detail', args=[order_items[0].id])
    if is_authenticated:
        user = order_items[0].order.profile
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        'assortment': {
            'id': assortment[0].id
        },
        'quantity': 1
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
def test_order_items_patch(api_client, token_factory, order_item_factory, is_authenticated, http_response):
    order_items = order_item_factory(_quantity=1)
    order_items[0].order.status = Order.Status.NEW
    order_items[0].order.save()
    order_items[0].assortment.quantity = 2
    order_items[0].assortment.save()
    url = reverse('orderitem-detail', args=[order_items[0].id])
    if is_authenticated:
        user = order_items[0].order.profile
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        'quantity': 2
    }
    resp = api_client.patch(url, payload, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_204_NO_CONTENT),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_order_items_delete(api_client, token_factory, order_item_factory, is_authenticated, http_response):
    order_items = order_item_factory(_quantity=1)
    url = reverse('orderitem-detail', args=[order_items[0].id])
    if is_authenticated:
        user = order_items[0].order.profile
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url, format='json')
    assert resp.status_code == http_response