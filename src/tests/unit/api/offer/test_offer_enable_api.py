import pytest


@pytest.mark.django_db
def test_read_list(api_client) -> None:
    response = api_client.get("/api/v1/offers/enable/", format="json")
    assert response.status_code == 200
    assert response.data == [
        {
            "uuid": "7554b08f-dd43-4254-b695-c97c545f95ab",
            "title": "solo",
            "description": "Ne restez pas seul(e) chez vous !",
            "price": "1999.99",
            "ntickets": 1,
            "disable": False,
        },
        {
            "uuid": "b25d6938-c096-4cb5-8f53-8cb16412dcab",
            "title": "duo",
            "description": "Invitez votre ami(e) !",
            "price": "3499.99",
            "ntickets": 2,
            "disable": False,
        },
        {
            "uuid": "e098f441-c675-499a-aa3a-847f8bc2da53",
            "title": "familiale",
            "description": "Venez en famille !",
            "price": "6456.99",
            "ntickets": 4,
            "disable": False,
        },
    ]
