from decimal import Decimal
import pytest
from typing import Callable
import logging
from random import random
from math import floor

from django.core.management import call_command

from rest_framework.test import APIClient

from api.models import Discipline, Offer

logger = logging.getLogger(__name__)

# setttings:
dir_fixtures = "tests/unit/api/fixtures/"
fixtures = [
    "disciplines.json",
    "events.json",
    "offers.json",
]


@pytest.fixture(scope="package")
def django_db_setup(django_db_setup, django_db_blocker) -> None:
    logger.info('fixture(scope="package"): django_db_setup')
    with django_db_blocker.unblock():
        # load all the fixtures from settings
        for fixture in fixtures:
            call_command("loaddata", dir_fixtures + fixture)


@pytest.fixture(scope="function")
def api_client():
    yield APIClient()


@pytest.fixture
def get_2_dates_with_2_days_following_each_other() -> tuple[str, str]:
    """return a tuple with 2 dates and 2 days following each other"""
    return ("2024-09-22", "2024-09-23")


@pytest.fixture
def create_discipline_sample_fields() -> Callable:
    """return fields ready to create a discipline"""

    def _create_discipline_sample_fields() -> dict:
        # name field must be unique
        return {"name": f"sample {floor(random() * 100_000)}"}

    return _create_discipline_sample_fields


@pytest.fixture
def create_event_sample_fields(
    create_discipline_sample_fields: Callable,
    get_2_dates_with_2_days_following_each_other: tuple[str, str],
) -> Callable:
    """return fields ready to create an event"""

    def _create_event_sample_fields() -> dict:
        disc = Discipline.objects.create(**create_discipline_sample_fields())
        return {
            # title field must be unique
            "title": f"sample {floor(random() * 100_000)}",
            "begin_at": get_2_dates_with_2_days_following_each_other[0],
            "end_at": get_2_dates_with_2_days_following_each_other[1],
            "description": "sample description",
            "discipline": disc,
        }

    return _create_event_sample_fields


@pytest.fixture
def create_offer_sample_fields() -> Callable:
    """return fields ready to create an offer"""

    def _create_offer_sample_fields() -> dict:
        # title field must be unique
        fields = {
            "title": f"sample {floor(random() * 100_000)}",
            "description": "blabla",
            "price": Decimal(f"{floor(random() * 10_000)}.{floor(random() * 100)}"),
            "ntickets": floor(random() * 10) + 1,  # cant be 0
            "disable": False,
        }
        # for get a cleaned price field with the model method:
        offer = Offer(**fields)
        fields["price"] = offer.price
        return fields

    return _create_offer_sample_fields
