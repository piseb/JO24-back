import pytest
from typing import Callable

from django.forms import ValidationError
from django.db import IntegrityError

from apiv1.models import Discipline


@pytest.mark.django_db
def test_working(get_discipline_sample_fields: dict) -> None:
    Discipline(**get_discipline_sample_fields).save()


def test_str(get_discipline_sample_fields: dict) -> None:
    disc = Discipline(**get_discipline_sample_fields)
    assert str(disc) == get_discipline_sample_fields["name"]


@pytest.mark.django_db
def test_name_must_be_unique_and_the_exception_message(
    create_discipline_sample_fields: Callable,
):
    event1, event2 = (
        create_discipline_sample_fields(),
        create_discipline_sample_fields(),
    )
    event1["name"] = event2["name"] = "my unique name"
    Discipline.objects.create(**event1)
    with pytest.raises(
        IntegrityError, match="^duplicate key value violates unique constraint"
    ):
        Discipline.objects.create(**event2)


@pytest.mark.django_db
def test_name_must_be_not_empty_and_the_exception_message(
    get_discipline_sample_fields: dict,
) -> None:
    get_discipline_sample_fields["name"] = ""
    with pytest.raises(ValidationError) as excinfo:
        Discipline.objects.create(**get_discipline_sample_fields)
    assert str(excinfo.value) == "{'nom': ['Le nom est obligatoire.']}"
