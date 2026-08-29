"""Public interface of the SmartScore info client."""

from .api.nhle import NHLClient
from .models.player import (
    Player,
    PlayerInfo,
    PlayerStats,
    get_five_gpg,
    get_gpg,
    get_hgpg,
    get_hppg,
)
from .models.team import (
    GameTeam,
    TeamInfo,
    TeamStats,
    get_otga,
    get_otshga,
    get_tgpg,
)
from .schemas.player import PLAYER_INFO_SCHEMA
from .schemas.team import TEAM_INFO_SCHEMA
from .utility import exponential_backoff_request

__all__ = [
    "PLAYER_INFO_SCHEMA",
    "TEAM_INFO_SCHEMA",
    "GameTeam",
    "NHLClient",
    "Player",
    "PlayerInfo",
    "PlayerStats",
    "TeamInfo",
    "TeamStats",
    "exponential_backoff_request",
    "get_five_gpg",
    "get_gpg",
    "get_hgpg",
    "get_hppg",
    "get_otga",
    "get_otshga",
    "get_tgpg",
]
