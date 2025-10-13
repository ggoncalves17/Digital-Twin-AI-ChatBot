from digital_twin.schemas.hobby import HobbyBase, HobbyType, HobbyFrequency

def test_valid_hobby_schema():
    hobby = HobbyBase(
        name="Running",
        type=HobbyType.SPORTS_FITNESS,
        freq=HobbyFrequency.OFTEN
    )
    assert hobby.name == "Running"
    assert hobby.type == HobbyType.SPORTS_FITNESS

def test_invalid_name_raises_error():
    import pytest
    with pytest.raises(ValueError):
        HobbyBase(name="  ", type=HobbyType.GAMING_TECH, freq=HobbyFrequency.RARELY)
