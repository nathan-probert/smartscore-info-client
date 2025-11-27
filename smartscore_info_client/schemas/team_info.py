from dataclasses import dataclass, field

from marshmallow import Schema, fields
import ctypes
from utility import exponential_backoff_request


class TeamInfoC(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int),
        ("tgpg", ctypes.c_float),
        ("otga", ctypes.c_float),
    ]


@dataclass(frozen=True)
class TeamInfo:
    team_name: str
    team_abbr: str
    season: str
    team_id: int
    opponent_id: int
    home: bool

    tgpg: float = 0.0  # team goals per game
    otga: float = 0.0  # other team goals against
    otshga: float = 0.0  # other team shorthanded goals per game

    _class_data_summary: dict = field(init=False, default=None, repr=False)
    _class_data_penalties: dict = field(init=False, default=None, repr=False)

    def __post_init__(self):
        if TeamInfo._class_data_summary is None:
            URL = f"https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=seasonId={self.season}%20and%20gameTypeId=2"
            TeamInfo._class_data_summary = exponential_backoff_request(URL)

        if TeamInfo._class_data_penalties is None:
            URL = f"https://api.nhle.com/stats/rest/en/team/penaltykilltime?cayenneExp=seasonId={self.season}%20and%20gameTypeId=2"
            TeamInfo._class_data_penalties = exponential_backoff_request(URL)

        object.__setattr__(
            self, "tgpg", get_tgpg(TeamInfo._class_data_summary, self.team_id)
        )
        object.__setattr__(
            self, "otga", get_otga(TeamInfo._class_data_summary, self.opponent_id)
        )
        object.__setattr__(
            self, "otshga", get_otshga(TeamInfo._class_data_penalties, self.opponent_id)
        )


class TeamInfoSchema(Schema):
    team_name = fields.Str()
    team_abbr = fields.Str()
    season = fields.Str()
    team_id = fields.Int()
    opponent_id = fields.Int()

    tgpg = fields.Float()
    otga = fields.Float()
    otshga = fields.Float()
    home = fields.Bool()


TEAM_INFO_SCHEMA = TeamInfoSchema()


def get_tgpg(_data, team_id):
    for team in _data["data"]:
        if team["teamId"] == team_id:
            return team["goalsForPerGame"]
    return 0.0


def get_otga(_data, opponent_id):
    for team in _data["data"]:
        if team["teamId"] == opponent_id:
            return team["goalsAgainstPerGame"]
    return 0.0


def get_otshga(_data, opponent_id):
    for team in _data["data"]:
        if team["teamId"] == opponent_id:
            return team["shorthandedGoalsAgainst"] / team["gamesPlayed"]
    return 0.0
