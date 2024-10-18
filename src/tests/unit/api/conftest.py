import pytest
import logging
from random import random
from math import floor
from typing import Callable

from django.core.management import call_command

from rest_framework.test import APIClient

from api.models import Discipline

logger = logging.getLogger(__name__)


@pytest.fixture(scope="package")
def django_db_setup(django_db_setup, django_db_blocker) -> None:
    logger.info('fixture(scope="package"): django_db_setup')
    with django_db_blocker.unblock():
        call_command("loaddata", "tests/unit/api/fixture.json")


@pytest.fixture
def create_discipline_sample_fields() -> Callable:
    def _create_discipline_sample_fields() -> dict:
        # name field must be unique
        return {"name": f"sample {floor(random() * 100_000)}"}

    return _create_discipline_sample_fields


@pytest.fixture
def get_discipline_sample_fields(create_discipline_sample_fields) -> dict:
    return create_discipline_sample_fields()


@pytest.fixture
def create_event_sample_fields(
    create_discipline_sample_fields,
    get_date_with_2_days_following_each_other,
) -> Callable:
    def _create_event_sample_fields() -> dict:
        disc = Discipline.objects.create(**create_discipline_sample_fields())
        return {
            # title field must be unique
            "title": f"sample {floor(random() * 100_000)}",
            "begin_at": get_date_with_2_days_following_each_other[0],
            "end_at": get_date_with_2_days_following_each_other[1],
            "description": "sample description",
            "discipline": disc,
        }

    return _create_event_sample_fields


@pytest.fixture
def get_event_sample_fields(create_event_sample_fields) -> dict:
    return create_event_sample_fields()


@pytest.fixture
def get_date_with_2_days_following_each_other() -> tuple[str, str]:
    return ("2024-09-22", "2024-09-23")


@pytest.fixture(scope="function")
def api_client():
    yield APIClient()
