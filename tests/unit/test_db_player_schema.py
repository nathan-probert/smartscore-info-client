import pytest
from schemas.db_player_info import PlayerDbInfo, PlayerDbInfoSchema, PlayerDbInfoC

sample_data = {
    "_id": "621f4f4c7b3b3b0001f3b3b3",
    "date": "2024-02-16",
    "name": "Jaccob Slavin",
    "id": 8476958,
    "gpg": 0.08,
    "hgpg": 0.1,
    "five_gpg": 0.12,
    "team_name": "Carolina Hurricanes",
    "tgpg": 3.31,
    "otga": 2.87,
    "scored": 1,
    "home": True,
    "hppg": None,
    "otshga": None,
}


def test_player_db_info_schema_serialization():
    schema = PlayerDbInfoSchema()
    serialized_data = schema.dump(sample_data)

    assert serialized_data["_id"] == "621f4f4c7b3b3b0001f3b3b3"
    assert serialized_data["name"] == "Jaccob Slavin"
    assert serialized_data["id"] == 8476958
    assert serialized_data["team_name"] == "Carolina Hurricanes"
    assert serialized_data["gpg"] == pytest.approx(0.08, rel=1e-6)
    assert serialized_data["hgpg"] == pytest.approx(0.1, rel=1e-6)
    assert serialized_data["five_gpg"] == pytest.approx(0.12, rel=1e-6)
    assert serialized_data["tgpg"] == pytest.approx(3.31, rel=1e-6)
    assert serialized_data["otga"] == pytest.approx(2.87, rel=1e-6)
    assert serialized_data["scored"] == 1
    assert serialized_data["home"] is True
    assert serialized_data["hppg"] is None
    assert serialized_data["otshga"] is None


def test_player_db_info_initialization():
    player_info = PlayerDbInfo(
        _id="621f4f4c7b3b3b0001f3b3b3",
        date="2024-02-16",
        name="Jaccob Slavin",
        id=8476958,
        gpg=0.08,
        hgpg=0.1,
        five_gpg=0.12,
        team_name="Carolina Hurricanes",
        tgpg=3.31,
        otga=2.87,
        scored=1,
        home=True,
    )

    assert player_info._id == "621f4f4c7b3b3b0001f3b3b3"
    assert player_info.date == "2024-02-16"
    assert player_info.name == "Jaccob Slavin"
    assert player_info.id == 8476958
    assert player_info.gpg == pytest.approx(0.08, rel=1e-6)
    assert player_info.hgpg == pytest.approx(0.1, rel=1e-6)
    assert player_info.five_gpg == pytest.approx(0.12, rel=1e-6)
    assert player_info.team_name == "Carolina Hurricanes"
    assert player_info.tgpg == pytest.approx(3.31, rel=1e-6)
    assert player_info.otga == pytest.approx(2.87, rel=1e-6)
    assert player_info.scored == 1
    assert player_info.home is True
    assert player_info.hppg is None
    assert player_info.otshga is None


def test_player_db_info_c_structure():
    player_info_c = PlayerDbInfoC(
        date=b"2024-02-16",
        name=b"Jaccob Slavin",
        gpg=0.08,
        hgpg=0.1,
        five_gpg=0.12,
        tgpg=3.31,
        otga=2.87,
    )

    assert player_info_c.date == b"2024-02-16"
    assert player_info_c.name == b"Jaccob Slavin"
    assert player_info_c.gpg == pytest.approx(0.08, rel=1e-6)
    assert player_info_c.hgpg == pytest.approx(0.1, rel=1e-6)
    assert player_info_c.five_gpg == pytest.approx(0.12, rel=1e-6)
    assert player_info_c.tgpg == pytest.approx(3.31, rel=1e-6)
    assert player_info_c.otga == pytest.approx(2.87, rel=1e-6)


def test_optional_fields():
    player_info = PlayerDbInfo(
        _id="621f4f4c7b3b3b0001f3b3b3",
        date="2024-02-16",
        name="Jaccob Slavin",
        id=8476958,
        gpg=0.08,
        hgpg=0.1,
        five_gpg=0.12,
        team_name="Carolina Hurricanes",
        tgpg=3.31,
        otga=2.87,
        scored=1,
    )

    assert player_info.hppg is None
    assert player_info.otshga is None
    assert player_info.home is None

    serialized_data = PlayerDbInfoSchema().dump(player_info)
    assert serialized_data["hppg"] is None
    assert serialized_data["otshga"] is None
    assert serialized_data["home"] is None
