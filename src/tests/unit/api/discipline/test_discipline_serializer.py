import pytest
from typing import Callable

from rest_framework.renderers import JSONRenderer

from api.models import Discipline
from api.serializers import DisciplineSerializer


@pytest.mark.django_db
def test_discipline_serialized_to_json(
    create_discipline_sample_fields: Callable,
) -> None:
    disc_sample_fields = create_discipline_sample_fields()
    disc_sample = Discipline.objects.create(**disc_sample_fields)
    disc_sample_serialized = DisciplineSerializer(disc_sample)
    json = JSONRenderer().render(disc_sample_serialized.data)
    assert (
        json
        == f'{{"uuid":"{disc_sample.uuid}","name":"{disc_sample_fields["name"]}"}}'.encode()
    )
