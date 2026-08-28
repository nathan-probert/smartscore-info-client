from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GameTeam:
    """Identity of a team playing on a given day."""

    team_name: str
    team_abbr: str
    season: str
    team_id: int
    opponent_id: int
    home: bool = False

    @classmethod
    def from_mapping(cls, data) -> GameTeam:
        return cls(
            team_name=data["team_name"],
            team_abbr=data["team_abbr"],
            season=data["season"],
            team_id=data["team_id"],
            opponent_id=data["opponent_id"],
            home=data["home"],
        )


@dataclass(frozen=True)
class TeamStats:
    """Team-level features used when predicting whether a player will score."""

    tgpg: float = 0.0  # team goals per game
    otga: float = 0.0  # opponent team goals against per game
    otshga: float = 0.0  # opponent team shorthanded goals per game

    @classmethod
    def from_payloads(cls, summary, penalty_kill, team_id, opponent_id) -> TeamStats:
        return cls(
            tgpg=get_tgpg(summary, team_id),
            otga=get_otga(summary, opponent_id),
            otshga=get_otshga(penalty_kill, opponent_id),
        )


@dataclass(frozen=True)
class TeamInfo:
    """Composite of a team's identity and their stats."""

    team: GameTeam
    stats: TeamStats = field(default_factory=TeamStats)

    @property
    def team_name(self) -> str:
        return self.team.team_name

    @property
    def team_abbr(self) -> str:
        return self.team.team_abbr

    @property
    def season(self) -> str:
        return self.team.season

    @property
    def team_id(self) -> int:
        return self.team.team_id

    @property
    def opponent_id(self) -> int:
        return self.team.opponent_id

    @property
    def home(self) -> bool:
        return self.team.home

    @property
    def tgpg(self) -> float:
        return self.stats.tgpg

    @property
    def otga(self) -> float:
        return self.stats.otga

    @property
    def otshga(self) -> float:
        return self.stats.otshga


def get_tgpg(data, team_id):
    for team in data["data"]:
        if team["teamId"] == team_id:
            return team["goalsForPerGame"]
    return 0.0


def get_otga(data, opponent_id):
    for team in data["data"]:
        if team["teamId"] == opponent_id:
            return team["goalsAgainstPerGame"]
    return 0.0


def get_otshga(data, opponent_id):
    for team in data["data"]:
        if team["teamId"] == opponent_id:
            return team["shorthandedGoalsAgainst"] / team["gamesPlayed"]
    return 0.0
