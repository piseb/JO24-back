import pytest


@pytest.mark.django_db
def test_read_list(api_client) -> None:
    response = api_client.get("/api/v1/disciplines/", format="json")
    assert response.status_code == 200
    assert response.data == [
        {"uuid": "22899b0d-72af-4fcd-af3f-2aaa94eedfd8", "name": "Athlétisme"},
        {"uuid": "2c73e848-a0e3-4900-8a84-01e27ae09ba1", "name": "Judo"},
    ]


@pytest.mark.django_db
def test_read(api_client) -> None:
    response = api_client.get(
        "/api/v1/disciplines/2c73e848-a0e3-4900-8a84-01e27ae09ba1/", format="json"
    )
    assert response.status_code == 200
    assert response.data == {
        "uuid": "2c73e848-a0e3-4900-8a84-01e27ae09ba1",
        "name": "Judo",
    }

    response = api_client.get("/api/v1/disciplines/1/", format="json")
    assert response.status_code == 404
