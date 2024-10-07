import pytest
from schemas.player_info import PlayerInfo


@pytest.fixture
def player_info_with_stats():
  yield PlayerInfo(
    name="John Doe",
    id=8478402,
    team_id=12,
    gpg=0.5,
    hgpg=0.55,
    five_gpg=0.6,
  )


@pytest.fixture
def mock_teams_api_response():
  return {
    "data": [
      {"teamId": 12, "goalsForPerGame": 3.2, "goalsAgainstPerGame": 2.5},
      {"teamId": 34, "goalsForPerGame": 2.8, "goalsAgainstPerGame": 3.1},
    ]
  }


@pytest.fixture
def mock_players_api_response():
  return {
    "seasonTotals": [
      {"season": "20232024", "leagueAbbrev": "NHL", "goals": 20, "gamesPlayed": 40},
      {"season": "20222023", "leagueAbbrev": "NHL", "goals": 25, "gamesPlayed": 50},
      {"season": "20212022", "leagueAbbrev": "NHL", "goals": 30, "gamesPlayed": 60},
    ],
    "last5Games": [
      {"goals": 1},
      {"goals": 2},
      {"goals": 0},
      {"goals": 3},
      {"goals": 1},
    ],
  }
