import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.reverse import reverse

from profile.models import User


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_200_OK),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_feature_list(api_client, user_factory, token_factory, feature_factory, is_authenticated, http_response):
    feature = feature_factory(_quantity=1)
    url = reverse('feature-list')
    if is_authenticated:
        user = user_factory(user_type=User.Type.CUSTOMER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.get(url, format='json')
    assert resp.status_code == http_response


@pytest.mark.parametrize(
    ["is_authenticated", "http_response"],
    (
        (True, HTTP_201_CREATED),
        (None, HTTP_401_UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_feature_post(api_client, user_factory, token_factory, is_authenticated, http_response):
    url = reverse('feature-list')
    if is_authenticated:
        user = user_factory(user_type=User.Type.PROVIDER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "name": "test",
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
def test_feature_detail(api_client, user_factory, token_factory, feature_factory, is_authenticated, http_response):
    feature = feature_factory(_quantity=1)
    url = reverse('feature-detail', args=[feature[0].id])
    if is_authenticated:
        user = user_factory(user_type=User.Type.PROVIDER)
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
def test_feature_put(api_client, user_factory, token_factory, feature_factory, is_authenticated, http_response):
    feature = feature_factory(_quantity=1)
    url = reverse('feature-detail', args=[feature[0].id])
    if is_authenticated:
        user = user_factory(user_type=User.Type.PROVIDER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "name": "test",
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
def test_feature_patch(api_client, user_factory, token_factory, feature_factory, is_authenticated, http_response):
    feature = feature_factory(_quantity=1)
    url = reverse('feature-detail', args=[feature[0].id])
    if is_authenticated:
        user = user_factory(user_type=User.Type.PROVIDER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    payload = {
        "name": "test",
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
def test_feature_delete(api_client, user_factory, token_factory, feature_factory, is_authenticated, http_response):
    feature = feature_factory(_quantity=1)
    url = reverse('feature-detail', args=[feature[0].id])
    if is_authenticated:
        user = user_factory(user_type=User.Type.PROVIDER)
        token = token_factory(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp = api_client.delete(url, format='json')
    assert resp.status_code == http_response