import pytest
from typing import Callable

from django.db import IntegrityError

from api.models import Discipline


@pytest.mark.django_db
def test_working(create_discipline_sample_fields: Callable) -> None:
    Discipline(**create_discipline_sample_fields()).save()


def test_str(create_discipline_sample_fields: Callable) -> None:
    discipline_sample_fields = create_discipline_sample_fields()
    discipline = Discipline(**discipline_sample_fields)
    assert str(discipline) == discipline_sample_fields["name"]


@pytest.mark.django_db
def test_name_must_be_unique_and_the_exception_message(
    create_discipline_sample_fields: Callable,
):
    discipline_1_sample_fields, discipline_2_sample_fields = (
        create_discipline_sample_fields(),
        create_discipline_sample_fields(),
    )
    discipline_1_sample_fields["name"] = discipline_2_sample_fields["name"] = (
        "my unique name"
    )
    Discipline.objects.create(**discipline_1_sample_fields)
    with pytest.raises(
        IntegrityError, match="^duplicate key value violates unique constraint"
    ):
        Discipline.objects.create(**discipline_2_sample_fields)
