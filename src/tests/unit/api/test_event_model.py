import pytest
from typing import Callable

from django.core.exceptions import ValidationError

from api.models import Event


@pytest.mark.django_db
def test_str(create_event_sample_fields: Callable) -> None:
    event_sample_fields = create_event_sample_fields()
    event_sample = Event(**event_sample_fields)
    assert (
        str(event_sample)
        == f"{event_sample_fields["title"]} ({event_sample_fields["begin_at"]}/{event_sample_fields["end_at"]}): {event_sample_fields["description"][:5]}"
    )


@pytest.mark.django_db
def test_begin_at_must_be_not_after_end_at_and_the_exception_message(
    create_event_sample_fields: Callable,
    get_2_dates_with_2_days_following_each_other: tuple[str, str],
) -> None:
    event_sample_fields = create_event_sample_fields()
    # end before begin
    event_sample_fields["end_at"], event_sample_fields["begin_at"] = (
        get_2_dates_with_2_days_following_each_other[0],
        get_2_dates_with_2_days_following_each_other[1],
    )

    with pytest.raises(ValidationError) as excinfo:
        Event.objects.create(**event_sample_fields)
    assert (
        str(excinfo.value) == "{'end_at': ['end_at must be equal or after begin_at']}"
    )


@pytest.mark.django_db
def test_end_at_can_be_after_or_same_than_end_at(
    create_event_sample_fields: Callable,
    get_2_dates_with_2_days_following_each_other: tuple[str, str],
) -> None:

    event_1_sample_fields, event_2_sample_fields = (
        create_event_sample_fields(),
        create_event_sample_fields(),
    )
    del (
        event_1_sample_fields["begin_at"],
        event_1_sample_fields["end_at"],
        event_2_sample_fields["begin_at"],
        event_2_sample_fields["end_at"],
    )

    date1, date2 = (
        get_2_dates_with_2_days_following_each_other[0],
        get_2_dates_with_2_days_following_each_other[1],
    )

    # can be same
    Event.objects.create(begin_at=date1, end_at=date1, **event_1_sample_fields)

    # can be after
    Event.objects.create(begin_at=date1, end_at=date2, **event_2_sample_fields)
