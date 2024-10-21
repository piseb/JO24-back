import pytest
from typing import Callable

from django.db import IntegrityError

from api.models import Offer


@pytest.mark.django_db
def test_working(create_offer_sample_fields: Callable) -> None:
    Offer(**create_offer_sample_fields()).save()


def test_str(create_offer_sample_fields: Callable) -> None:
    offer_sample_fields = create_offer_sample_fields()
    offer = Offer(**offer_sample_fields)
    assert (
        str(offer)
        == f'{offer_sample_fields["title"]} ({offer_sample_fields["price"]}€ / {offer_sample_fields["ntickets"]} tickets): {offer_sample_fields["description"][:5]}'
    )


@pytest.mark.django_db
def test_title_must_be_unique_and_the_exception_message(
    create_offer_sample_fields: Callable,
):
    offer_1_sample_fields, offer_2_sample_fields = (
        create_offer_sample_fields(),
        create_offer_sample_fields(),
    )
    offer_1_sample_fields["title"] = offer_2_sample_fields["title"] = "my unique title"
    Offer.objects.create(**offer_1_sample_fields)
    with pytest.raises(
        IntegrityError, match="^duplicate key value violates unique constraint"
    ):
        Offer.objects.create(**offer_2_sample_fields)
