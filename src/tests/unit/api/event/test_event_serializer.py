import pytest
from typing import Callable

from rest_framework.renderers import JSONRenderer

from api.models import Discipline, Event
from api.serializers import EventSerializer


@pytest.mark.django_db
def test_serialized_to_json(create_event_sample_fields: Callable) -> None:
    event_sample_fields = create_event_sample_fields()
    event_sample = Event.objects.create(**event_sample_fields)
    discipline_event_sample = Discipline.objects.get(uuid=event_sample.discipline.uuid)
    event_serialized = EventSerializer(event_sample)
    json = JSONRenderer().render(event_serialized.data)
    assert (
        json
        == f'{{"uuid":"{str(event_sample.uuid)}","discipline":{{"uuid":"{str(discipline_event_sample.uuid)}","name":"{discipline_event_sample.name}"}},"title":"{event_sample_fields["title"]}","begin_at":"{event_sample_fields["begin_at"]}","end_at":"{event_sample_fields["end_at"]}","description":"{event_sample_fields["description"]}"}}'.encode()
    )
