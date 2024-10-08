from dataclasses import dataclass, field

import requests
from marshmallow import Schema, fields
import ctypes


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

  tgpg: float = 0.0
  otga: float = 0.0

  _class_data_summary: dict = field(init=False, default=None, repr=False)

  def __post_init__(self):
    if TeamInfo._class_data_summary is None:
      URL = "https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=seasonId=20232024%20and%20gameTypeId=2"
      # URL = f"https://api.nhle.com/stats/rest/en/team/summary?cayenneExp=seasonId={self.season}%20and%20gameTypeId=2"
      TeamInfo._class_data_summary = requests.get(URL, timeout=10).json()

    object.__setattr__(
      self, "tgpg", get_tgpg(TeamInfo._class_data_summary, self.team_id)
    )
    object.__setattr__(
      self, "otga", get_otga(TeamInfo._class_data_summary, self.opponent_id)
    )


class TeamInfoSchema(Schema):
  team_name = fields.Str()
  team_abbr = fields.Str()
  season = fields.Str()
  team_id = fields.Int()
  opponent_id = fields.Int()

  tgpg = fields.Float()
  otga = fields.Float()


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
