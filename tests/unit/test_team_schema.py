from unittest.mock import patch
from schemas.team_info import TeamInfo, get_tgpg, get_otga


@patch("schemas.team_info.requests.get")
def test_team_info_initialization(mock_get, mock_teams_api_response):
  mock_get.return_value.json.return_value = mock_teams_api_response

  team = TeamInfo(name="Team A", abbr="TA", season="20232024", id=12, opponent_id=34)

  assert team.tgpg == 3.2
  assert team.otga == 3.1


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
