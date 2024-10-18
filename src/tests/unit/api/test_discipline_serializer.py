import pytest

from rest_framework.renderers import JSONRenderer

from api.models import Discipline
from api.serializers import DisciplineSerializer


@pytest.mark.django_db
def test_discipline_serialized_to_json(get_discipline_sample_fields: dict) -> None:
    disc_sample = Discipline.objects.create(**get_discipline_sample_fields)
    disc_sample_serialized = DisciplineSerializer(disc_sample)
    json = JSONRenderer().render(disc_sample_serialized.data)
    assert json == f'{{"id":"{disc_sample.id}","name":"{disc_sample.name}"}}'.encode()
