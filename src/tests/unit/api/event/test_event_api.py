import pytest


@pytest.mark.django_db
def test_read_list(api_client) -> None:
    response = api_client.get("/api/v1/events/", format="json")
    assert response.status_code == 200
    assert response.data == [
        {
            "uuid": "3f2d685e-7103-40d5-838d-96a54888553f",
            "discipline": {
                "uuid": "22899b0d-72af-4fcd-af3f-2aaa94eedfd8",
                "name": "Athlétisme",
            },
            "title": "ouverture",
            "begin_at": "2024-09-22",
            "end_at": "2024-09-23",
            "description": "Evénement d'ouverture.",
        },
        {
            "uuid": "11649f74-887c-4ea1-b628-d4793134e953",
            "discipline": {
                "uuid": "2c73e848-a0e3-4900-8a84-01e27ae09ba1",
                "name": "Judo",
            },
            "title": "fermeture",
            "begin_at": "2024-09-22",
            "end_at": "2024-09-23",
            "description": "Evénement d'ouverture.",
        },
    ]


@pytest.mark.django_db
def test_read(api_client) -> None:
    response = api_client.get(
        "/api/v1/events/11649f74-887c-4ea1-b628-d4793134e953/", format="json"
    )
    assert response.status_code == 200
    assert response.data == {
        "uuid": "11649f74-887c-4ea1-b628-d4793134e953",
        "discipline": {
            "uuid": "2c73e848-a0e3-4900-8a84-01e27ae09ba1",
            "name": "Judo",
        },
        "title": "fermeture",
        "begin_at": "2024-09-22",
        "end_at": "2024-09-23",
        "description": "Evénement d'ouverture.",
    }

    response = api_client.get("/api/v1/events/1/", format="json")
    assert response.status_code == 404
