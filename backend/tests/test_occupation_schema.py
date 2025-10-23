
from datetime import date

from digital_twin.schemas.occupation import (
    OccupationBase,
    OccupationUpdate,
)


def test_valid_occupation_schema():
    occupation = OccupationBase(
        position="Software Engineer",
        workplace="Tech Corp",
        date_started=date(2020, 1, 1),
        date_finished=date(2022, 1, 1)
    )
    assert occupation.position == "Software Engineer"
    assert occupation.workplace == "Tech Corp"
    assert occupation.date_started == date(2020, 1, 1)
    assert occupation.date_finished == date(2022, 1, 1)

def test_invalid_name_raises_error():
    import pytest
    with pytest.raises(ValueError):
        OccupationBase(position="  ", workplace="Tech Corp", date_started="2020-01-01", date_finished="2022-01-01")

def test_update_occupation_schema():
    occupation_update = OccupationUpdate(
        position="Senior Software Engineer",
    )
    assert occupation_update.position == "Senior Software Engineer"
    assert occupation_update.workplace is None
    assert occupation_update.date_started is None
    assert occupation_update.date_finished is None
