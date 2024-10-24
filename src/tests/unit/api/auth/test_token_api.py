import pytest
import json


@pytest.mark.django_db
def test_login(api_client) -> None:
    credentials = {
        "username": "user",
        "password": "useruser89",
    }
    response = api_client.post(
        "/api/v1/login/", json.dumps(credentials), content_type="application/json"
    )
    assert response.status_code == 200

    try:
        # token must to be here
        json.loads(response.content)["token"]
    except Exception as excinfo:
        pytest.fail(f"token dont exist: {excinfo}")

    credentials = {
        "username": "aaaaaaaaaaaaa",
        "password": "aaaaaaaaaaaaa",
    }
    response = api_client.post(
        "/api/v1/login/", json.dumps(credentials), content_type="application/json"
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_logout(api_client) -> None:
    token_from_fixture = "865bf2a9594abde947c5b6885c290144c2d03387"
    headers = {"Authorization": "Token " + token_from_fixture}
    response = api_client.get("/api/v1/logout/", headers=headers)
    assert response.status_code == 200

    # token removed so have to be 401
    response = api_client.get("/api/v1/logout/", headers=headers)
    assert response.status_code == 401
