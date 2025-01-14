import pytest
from schemas.db_player_info import PlayerDbInfo, PlayerDbInfoSchema, PlayerDbInfoC

sample_data = {
    "date": "2024-02-16",
    "name": "Jaccob Slavin",
    "id": 8476958,
    "team_id": 12,
    "gpg": 0.08,
    "hgpg": 0.1,
    "five_gpg": 0.12,
    "team_name": "Carolina Hurricanes",
    "team_abbr": "CAR",
    "tgpg": 3.31,
    "otga": 2.87,
    "stat": 0.5,
}


def test_player_db_info_schema_serialization():
    schema = PlayerDbInfoSchema()
    serialized_data = schema.dump(sample_data)

    assert serialized_data["name"] == "Jaccob Slavin"
    assert serialized_data["id"] == 8476958
    assert serialized_data["team_id"] == 12
    assert serialized_data["gpg"] == 0.08
    assert serialized_data["hgpg"] == 0.1
    assert serialized_data["five_gpg"] == 0.12
    assert serialized_data["stat"] == 0.5


def test_player_db_info_initialization():
    player_info = PlayerDbInfo(
        date="2024-02-16",
        name="Jaccob Slavin",
        id=8476958,
        team_id=12,
        gpg=0.08,
        hgpg=0.1,
        five_gpg=0.12,
        team_name="Carolina Hurricanes",
        team_abbr="CAR",
        tgpg=3.31,
        otga=2.87,
        stat=0.5,
    )

    assert player_info.name == "Jaccob Slavin"
    assert player_info.id == 8476958
    assert player_info.team_id == 12
    assert player_info.gpg == 0.08
    assert player_info.hgpg == 0.1
    assert player_info.five_gpg == 0.12
    assert player_info.team_name == "Carolina Hurricanes"
    assert player_info.team_abbr == "CAR"
    assert player_info.tgpg == 3.31
    assert player_info.otga == 2.87
    assert player_info.stat == 0.5


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
