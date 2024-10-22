from typing import Callable
from api.models import Offer


def test_str_disabled(create_offer_sample_fields: Callable) -> None:
    offer_sample_fields = create_offer_sample_fields()
    offer_sample_fields["disable"] = True
    offer = Offer(**offer_sample_fields)
    assert (
        str(offer)
        == f'DISABLE: {offer_sample_fields["title"]} ({offer_sample_fields["price"]}€ / {offer_sample_fields["ntickets"]} tickets): {offer_sample_fields["description"][:5]}'
    )
