import pytest

from rest_framework.renderers import JSONRenderer

from api.models import Discipline, Event
from api.serializers import EventSerializer


@pytest.mark.django_db
def test_serialized_to_json(get_event_sample_fields: dict) -> None:
    event = Event.objects.create(**get_event_sample_fields)
    discipline = Discipline.objects.last()
    event_serialized = EventSerializer(event)
    json = JSONRenderer().render(event_serialized.data)
    assert (
        json
        == f'{{"uuid":"{str(event.uuid)}","discipline":{{"uuid":"{str(discipline.uuid)}","name":"{discipline.name}"}},"title":"{get_event_sample_fields["title"]}","begin_at":"{get_event_sample_fields["begin_at"]}","end_at":"{get_event_sample_fields["end_at"]}","description":"{get_event_sample_fields["description"]}"}}'.encode()
    )
