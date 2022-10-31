from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from oauth2_provider.models import get_application_model
from social_core.exceptions import AuthCanceled

Application = get_application_model()


@pytest.fixture
def user():
    return get_user_model().objects.create(email="user@gmail.com")


def client_id(client_type=Application.CLIENT_PUBLIC, grant_type=Application.GRANT_AUTHORIZATION_CODE):
    return Application.objects.create(
        name="app", client_type=client_type, authorization_grant_type=grant_type
    ).client_id


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_type,grant_type",
    (
        (Application.CLIENT_CONFIDENTIAL, Application.GRANT_IMPLICIT),
        (Application.CLIENT_CONFIDENTIAL, Application.GRANT_AUTHORIZATION_CODE),
        (Application.CLIENT_CONFIDENTIAL, Application.GRANT_PASSWORD),
        (Application.CLIENT_CONFIDENTIAL, Application.GRANT_CLIENT_CREDENTIALS),
    ),
)
@pytest.mark.parametrize("data", [{"token": "access_token"}, {"code": "auth_code"}])
def test_invalid_client_id(client_type, grant_type, client, user, data, monkeypatch):
    monkeypatch.setattr(
        "social_django.utils.load_backend",
        mock.Mock(**{"return_value.complete.return_value": user, "return_value.do_auth.return_value": user}),
    )

    response = client.post(
        reverse("social_oauth_token:token", kwargs={"backend": "apple-id"}),
        data={**data, "client_id": client_id(client_type, grant_type)},
    )
    assert response.status_code == 400
    assert "message" in response.json()


@pytest.mark.parametrize(
    "data",
    (
        None,
        {"code": ""},
        {"token": ""},
        {"client_id": ""},
        {"code": "", "client_id": ""},
        {"token": "", "client_id": ""},
        {"code": "ldfjsk", "client_id": ""},
        {"token": "ldfjsk", "client_id": ""},
        {"code": "", "client_id": "sldfkjldkfj"},
        {"token": "", "client_id": "sldfkjldkfj"},
    ),
)
def test_invalid_request_body(data, client):
    assert (
        client.post(reverse("social_oauth_token:token", kwargs={"backend": "apple-id"}), data=data).status_code == 400
    )


@pytest.mark.django_db
@pytest.mark.parametrize("data", [{"token": "access_token"}, {"code": "auth_code"}])
def test_view(client, user, monkeypatch, data):
    monkeypatch.setattr(
        "social_django.utils.load_backend",
        mock.Mock(**{"return_value.complete.return_value": user, "return_value.do_auth.return_value": user}),
    )

    res = client.post(
        reverse("social_oauth_token:token", kwargs={"backend": "apple-id"}), data={**data, "client_id": client_id()}
    )

    assert res.status_code == 200
    assert len(client.session.items()) == 0

    token = res.json()
    for field in ("access_token", "expires_in", "token_type", "refresh_token"):
        assert field in token

    client.logout()
    assert client.get(reverse("profile")).status_code == 302
    assert client.get(reverse("profile"), HTTP_AUTHORIZATION=f"Bearer {token['access_token']}").status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("data", [{"token": "access_token"}, {"code": "auth_code"}])
def test_view_auth_exception(client, data, monkeypatch):
    monkeypatch.setattr(
        "social_django.utils.load_backend",
        mock.Mock(
            **{
                "return_value.complete.side_effect": AuthCanceled("apple-id"),
                "return_value.do_auth.side_effect": AuthCanceled("apple-id"),
            }
        ),
    )
    assert (
        client.post(
            reverse("social_oauth_token:token", kwargs={"backend": "apple-id"}),
            data={**data, "client_id": client_id()},
        ).status_code
        == 400
    )
