from unittest.mock import patch

from smartscore_info_client.api.nhle import NHLClient
from smartscore_info_client.models.player import (
    Player,
    PlayerInfo,
    get_five_gpg,
    get_gpg,
    get_hgpg,
)
from smartscore_info_client.schemas.player import PLAYER_INFO_SCHEMA


@patch("smartscore_info_client.api.nhle.exponential_backoff_request")
def test_get_player_stats(mock_request, mock_players_api_response):
    mock_request.return_value = mock_players_api_response

    client = NHLClient()
    stats = client.get_player_stats(8478402)

    assert stats.gpg == 0.5
    assert stats.hgpg == (20 + 25 + 30) / (40 + 50 + 60)
    assert stats.five_gpg == 1.4
    assert stats.hppg == (5 + 7 + 8) / (40 + 50 + 60)


def test_get_gpg(mock_players_api_response):
    gpg = get_gpg(mock_players_api_response)
    assert gpg == 25 / 50


def test_get_hgpg(mock_players_api_response):
    hgpg = get_hgpg(mock_players_api_response, years=3)
    assert hgpg == (20 + 25 + 30) / (40 + 50 + 60)


def test_get_five_gpg(mock_players_api_response):
    five_gpg = get_five_gpg(mock_players_api_response)
    assert five_gpg == (1 + 2 + 0 + 3 + 1) / 5


def test_player_info_schema_dump(player_info_with_stats):
    data = PLAYER_INFO_SCHEMA.dump(player_info_with_stats)

    assert data["name"] == "John Doe"
    assert data["id"] == 8478402
    assert data["team_id"] == 12
    assert data["gpg"] == 0.5
    assert data["hgpg"] == 0.55
    assert data["five_gpg"] == 0.6
    assert data["hppg"] == 0.2


def test_player_stats_empty_payload():
    stats = PlayerInfo(player=Player(name="John Doe", id=8478402, team_id=12)).stats

    assert stats.gpg == 0.0
    assert stats.hgpg == 0.0
    assert stats.five_gpg == 0.0
    assert stats.hppg == 0.0
