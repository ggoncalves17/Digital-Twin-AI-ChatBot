from digital_twin.schemas.hobby import HobbyBase, HobbyFrequency, HobbyType, HobbyUpdate


def test_valid_hobby_schema():
    hobby = HobbyBase(
        name="Running",
        type=HobbyType.SPORTS_FITNESS,
        freq=HobbyFrequency.OFTEN
    )
    assert hobby.name == "Running"
    assert hobby.type == HobbyType.SPORTS_FITNESS
    assert hobby.freq == HobbyFrequency.OFTEN

def test_invalid_name_raises_error():
    import pytest
    with pytest.raises(ValueError):
        HobbyBase(name="  ", type=HobbyType.GAMING_TECH, freq=HobbyFrequency.RARELY)

def test_update_hobby_schema():
    hobby_update = HobbyUpdate(
        name="Cycling",
    )
    assert hobby_update.name == "Cycling"
    assert hobby_update.type is None 
    assert hobby_update.freq is None
