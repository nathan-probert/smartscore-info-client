from unittest.mock import patch
from schemas.player_info import PlayerInfo, get_gpg, get_hgpg, get_five_gpg


def test_get_stats_on_initialization(mock_players_api_response):
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_players_api_response

        player = PlayerInfo(name="John Doe", id=8478402, team_id=12)

        assert player.gpg == 0.5
        assert player.hgpg == 0.5
        assert player.five_gpg == 1.4


@patch("schemas.player_info.requests.get")
def test_manual_stat_update(mock_get, player_info_with_stats):
    player = player_info_with_stats

    assert player.gpg == 0.5
    assert player.hgpg == 0.55
    assert player.five_gpg == 0.6


@patch("schemas.player_info.requests.get")
def test_get_gpg(mock_get, mock_players_api_response):
    mock_get.return_value.json.return_value = mock_players_api_response

    gpg = get_gpg(mock_players_api_response)
    assert gpg == 25 / 50


@patch("schemas.player_info.requests.get")
def test_get_hgpg(mock_get, mock_players_api_response):
    mock_get.return_value.json.return_value = mock_players_api_response

    hgpg = get_hgpg(mock_players_api_response, years=3)
    assert hgpg == (20 + 25 + 30) / (40 + 50 + 60)


@patch("schemas.player_info.requests.get")
def test_get_five_gpg(mock_get, mock_players_api_response):
    mock_get.return_value.json.return_value = mock_players_api_response

    five_gpg = get_five_gpg(mock_players_api_response)
    assert five_gpg == (1 + 2 + 0 + 3 + 1) / 5
