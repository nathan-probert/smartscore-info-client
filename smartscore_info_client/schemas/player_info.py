from dataclasses import dataclass, field
import requests
from marshmallow import Schema, fields
import ctypes


class PlayerInfoC(ctypes.Structure):
    _fields_ = [
        ("gpg", ctypes.c_float),
        ("hgpg", ctypes.c_float),
        ("five_gpg", ctypes.c_float),
        ("tgpg", ctypes.c_float),
        ("otga", ctypes.c_float),
        ("hppg", ctypes.c_float),
        ("otshga", ctypes.c_float),
        ("is_home", ctypes.c_float),
        ("hppg_otshga", ctypes.c_float)
    ]


class TestingPlayerInfoC(ctypes.Structure):
    _fields_ = [
        ("gpg", ctypes.c_float),
        ("hgpg", ctypes.c_float),
        ("five_gpg", ctypes.c_float),
        ("tgpg", ctypes.c_float),
        ("otga", ctypes.c_float),
        ("hppg", ctypes.c_float),
        ("otshga", ctypes.c_float),
        ("is_home", ctypes.c_float),
        ("hppg_otshga", ctypes.c_float),
        ("scored", ctypes.c_float),
        ("tims", ctypes.c_float),
        ("date", ctypes.c_char_p),
    ]


@dataclass(frozen=True)
class PlayerInfo:
    name: str
    id: int
    team_id: int
    date: str = field(default=None)

    gpg: float = field(default=None)
    hgpg: float = field(default=None)
    five_gpg: float = field(default=None)
    hppg: float = field(default=None)

    tgpg: float = field(default=None)
    otga: float = field(default=None)
    otshga: float = field(default=None)
    is_home: bool = field(default=None)

    scored: int = field(default=None)

    stat: float = field(default=None)
    odds: float = field(default=None)
    tims: int = field(default=None)


    def __post_init__(self):
        if self.gpg is None:
            self.get_stats()

    def get_stats(self):
        URL = f"https://api-web.nhle.com/v1/player/{self.id}/landing"
        _data = requests.get(URL, timeout=3).json()

        object.__setattr__(self, "gpg", get_gpg(_data))
        object.__setattr__(self, "hgpg", get_hgpg(_data))
        object.__setattr__(self, "five_gpg", get_five_gpg(_data))
        object.__setattr__(self, "hppg", get_hppg(_data))


class PlayerInfoSchema(Schema):
    name = fields.Str()
    id = fields.Int()
    team_id = fields.Int()
    date = fields.Str(allow_none=True)

    gpg = fields.Float()
    hgpg = fields.Float()
    five_gpg = fields.Float()
    hppg = fields.Float()

    tgpg = fields.Float(allow_none=True)
    otga = fields.Float(allow_none=True)
    otshga = fields.Float(allow_none=True)
    is_home = fields.Bool(allow_none=True)

    scored = fields.Int(allow_none=True)

    stat = fields.Float(allow_none=True)
    odds = fields.Float(allow_none=True)
    tims = fields.Int(allow_none=True)


PLAYER_INFO_SCHEMA = PlayerInfoSchema()


def get_gpg(_data):
    return get_hgpg(_data, 1)


def get_hgpg(_data, years: int = 3):
    goals = 0
    games = 0

    cur_season = str(_data["seasonTotals"][-1]["season"])

    acceptable_seasons = get_acceptable_seasons(cur_season, years)
    for season_data in _data["seasonTotals"]:
        if (str(season_data["season"]) in acceptable_seasons) and season_data[
            "leagueAbbrev"
        ] == "NHL":
            goals += season_data["goals"]
            games += season_data["gamesPlayed"]

    return goals / games if games != 0 else 0.0


def get_hppg(_data, years: int = 3):
    ppg = 0
    games = 0

    cur_season = str(_data["seasonTotals"][-1]["season"])

    acceptable_seasons = get_acceptable_seasons(cur_season, years)
    for season_data in _data["seasonTotals"]:
        if (str(season_data["season"]) in acceptable_seasons) and season_data[
            "leagueAbbrev"
        ] == "NHL":
            print(f"season_data: {season_data}")
            ppg += season_data["powerPlayGoals"]
            games += season_data["gamesPlayed"]

    return ppg / games if games != 0 else 0.0


def get_five_gpg(_data):
    goals = 0
    games = 5

    try:
        for game_data in _data["last5Games"]:
            goals += game_data["goals"]
    except KeyError:
        return 0

    return goals / games


def get_acceptable_seasons(current_season: str, years: int) -> list:
    acceptable_seasons = []

    for _ in range(years):
        acceptable_seasons.append(current_season)
        current_season = get_previous_season(current_season)
    return acceptable_seasons


def get_previous_season(current_season: str) -> str:
    year_start = int(current_season[:4])
    year_end = int(current_season[4:])

    if year_end == 0:
        previous_season = f"{year_start - 1}9999"
    else:
        previous_season = f"{year_start - 1}{year_end - 1:02d}"
    return previous_season
