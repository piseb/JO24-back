import pytest
from typing import Callable

from rest_framework.renderers import JSONRenderer

from api.models import Offer
from api.serializers import OfferSerializer


@pytest.mark.django_db
def test_offer_serialized_to_json(
    create_offer_sample_fields: Callable,
) -> None:
    offer_sample_fields = create_offer_sample_fields()
    offer_sample = Offer.objects.create(**offer_sample_fields)
    offer_sample_serialized = OfferSerializer(offer_sample)
    json = JSONRenderer().render(offer_sample_serialized.data)
    assert (
        json
        == f'{{"uuid":"{offer_sample.uuid}","title":"{offer_sample_fields["title"]}","description":"{offer_sample_fields["description"]}","price":"{offer_sample_fields["price"]}","ntickets":{offer_sample_fields["ntickets"]},"disable":{"true" if offer_sample_fields["disable"] else "false"}}}'.encode()
    )
