from unittest.mock import patch

from smartscore_info_client.api.nhle import NHLClient
from smartscore_info_client.models.team import (
    GameTeam,
    TeamInfo,
    TeamStats,
    get_otga,
    get_otshga,
    get_tgpg,
)
from smartscore_info_client.schemas.team import TEAM_INFO_SCHEMA


@patch("smartscore_info_client.api.nhle.exponential_backoff_request")
def test_get_team_stats(mock_request, mock_teams_api_response):
    mock_request.return_value = mock_teams_api_response

    client = NHLClient()
    stats = client.get_team_stats("20232024", 12, 34)

    assert stats.tgpg == 3.2
    assert stats.otga == 3.1
    assert stats.otshga == 0.0125


def test_get_tgpg(mock_teams_api_response):
    tgpg = get_tgpg(mock_teams_api_response, 12)
    assert tgpg == 3.2

    tgpg = get_tgpg(mock_teams_api_response, 34)
    assert tgpg == 2.8

    tgpg = get_tgpg(mock_teams_api_response, 99)  # Non-existent team
    assert tgpg == 0.0


def test_get_otga(mock_teams_api_response):
    otga = get_otga(mock_teams_api_response, 12)
    assert otga == 2.5

    otga = get_otga(mock_teams_api_response, 34)
    assert otga == 3.1

    otga = get_otga(mock_teams_api_response, 99)  # Non-existent opponent
    assert otga == 0.0


def test_get_otshga(mock_teams_api_response):
    otshga = get_otshga(mock_teams_api_response, 12)
    assert otshga == 0.025

    otshga = get_otshga(mock_teams_api_response, 34)
    assert otshga == 0.0125

    otshga = get_otshga(mock_teams_api_response, 99)  # Non-existent opponent
    assert otshga == 0


def test_game_team_from_mapping():
    mapping = {
        "team_name": "Florida Panthers",
        "team_abbr": "FLA",
        "season": "20242025",
        "team_id": 13,
        "opponent_id": 14,
        "home": True,
    }

    team = GameTeam.from_mapping(mapping)

    assert team.team_name == "Florida Panthers"
    assert team.team_abbr == "FLA"
    assert team.season == "20242025"
    assert team.team_id == 13
    assert team.opponent_id == 14
    assert team.home is True


def test_team_info_schema_dump():
    team = GameTeam.from_mapping(
        {
            "team_name": "Florida Panthers",
            "team_abbr": "FLA",
            "season": "20242025",
            "team_id": 13,
            "opponent_id": 14,
            "home": True,
        }
    )
    team_info = TeamInfo(team=team, stats=TeamStats(tgpg=3.2, otga=3.1, otshga=0.5))
    data = TEAM_INFO_SCHEMA.dump(team_info)

    assert data["team_name"] == "Florida Panthers"
    assert data["team_id"] == 13
    assert data["home"] is True
    assert data["tgpg"] == 3.2
    assert data["otga"] == 3.1
    assert data["otshga"] == 0.5
