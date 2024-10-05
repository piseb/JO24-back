import pytest
from copy import deepcopy
from typing import Callable

from django.forms import ValidationError

from apiv1.models import Event, Discipline

@pytest.mark.django_db
def test_str(get_event_sample_fields: dict) -> None:
    event = Event(**get_event_sample_fields)
    assert str(event) == f"{get_event_sample_fields["title"]} ({get_event_sample_fields["begin_at"]}/{get_event_sample_fields["end_at"]}): {get_event_sample_fields["description"][:5]}"


@pytest.mark.django_db
def test_some_field_must_be_not_empty_and_the_exception_message(
    get_event_sample_fields: dict) -> None:

    event_fields_to_test = get_event_sample_fields
    disc = event_fields_to_test.pop("discipline")
    event_fields_not_to_test = {"discipline": disc}

    # we create an instance with good parameters,
    # so we can test with same parameters but only 1 field edited
    Event.objects.create(**event_fields_not_to_test, **event_fields_to_test)

    for field in event_fields_to_test:
        testing_parameters = deepcopy(event_fields_to_test)
        testing_parameters[field] = ""
        event = Event(**event_fields_not_to_test, **testing_parameters)
        with pytest.raises(ValidationError, match=f"^\\{{'{field}': \\['L[a|e] .* est obligatoire.'\\]\\}}"):
            event.save()


@pytest.mark.django_db
def test_begin_at_must_be_not_after_end_at_and_the_exception_message(
    get_event_sample_fields: dict,
    get_date_with_2_days_following_each_other: tuple[str, str]) -> None:

    # end before begin
    get_event_sample_fields["end_at"], get_event_sample_fields["begin_at"] = get_date_with_2_days_following_each_other[0], get_date_with_2_days_following_each_other[1]

    with pytest.raises(ValidationError) as excinfo:
        Event.objects.create(**get_event_sample_fields)
    assert str(excinfo.value) == "{'end_at': ['La date de fin doit être la même ou après la date de début.']}"


@pytest.mark.django_db
def test_end_at_can_be_after_or_same_than_end_at(
    create_event_sample_fields: Callable,
    get_date_with_2_days_following_each_other: tuple[str, str]) -> None:

    event1_fields, event2_fields = create_event_sample_fields(), create_event_sample_fields()
    del event1_fields["begin_at"], event1_fields["end_at"], event2_fields["begin_at"], event2_fields["end_at"],

    date1, date2 = get_date_with_2_days_following_each_other[0], get_date_with_2_days_following_each_other[1]

    # can be same
    Event.objects.create(begin_at=date1, end_at=date1, **event1_fields)

    # can be after
    Event.objects.create(begin_at=date1, end_at=date2, **event2_fields)
