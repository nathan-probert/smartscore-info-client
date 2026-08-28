from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Player:
    """Identity of a player."""

    name: str
    id: int
    team_id: int


@dataclass(frozen=True)
class PlayerStats:
    """Goal-scoring features used to predict whether a player will score."""

    gpg: float = 0.0
    hgpg: float = 0.0
    five_gpg: float = 0.0
    hppg: float = 0.0

    @classmethod
    def from_landing_payload(cls, payload, years: int = 3) -> PlayerStats:
        return cls(
            gpg=get_gpg(payload),
            hgpg=get_hgpg(payload, years),
            five_gpg=get_five_gpg(payload),
            hppg=get_hppg(payload, years),
        )


@dataclass(frozen=True)
class PlayerInfo:
    """Composite of a player's identity and their stats."""

    player: Player
    stats: PlayerStats = field(default_factory=PlayerStats)

    @property
    def name(self) -> str:
        return self.player.name

    @property
    def id(self) -> int:
        return self.player.id

    @property
    def team_id(self) -> int:
        return self.player.team_id

    @property
    def gpg(self) -> float:
        return self.stats.gpg

    @property
    def hgpg(self) -> float:
        return self.stats.hgpg

    @property
    def five_gpg(self) -> float:
        return self.stats.five_gpg

    @property
    def hppg(self) -> float:
        return self.stats.hppg


def get_gpg(data):
    return get_hgpg(data, 1)


def get_hgpg(data, years: int = 3):
    goals = 0
    games = 0

    season_totals = data.get("seasonTotals") or []

    cur_season = (
        str(season_totals[-1].get("season"))
        if season_totals
        and isinstance(season_totals[-1], dict)
        and "season" in season_totals[-1]
        else None
    )

    if not cur_season:
        return 0.0

    acceptable_seasons = get_acceptable_seasons(cur_season, years)
    for season_data in season_totals:
        if (str(season_data["season"]) in acceptable_seasons) and season_data[
            "leagueAbbrev"
        ] == "NHL":
            goals += season_data["goals"]
            games += season_data["gamesPlayed"]

    return goals / games if games != 0 else 0.0


def get_hppg(data, years: int = 3):
    ppg = 0
    games = 0

    season_totals = data.get("seasonTotals") or []
    if not season_totals:
        return 0.0

    cur_season = str(season_totals[-1]["season"])

    acceptable_seasons = get_acceptable_seasons(cur_season, years)
    for season_data in season_totals:
        if (str(season_data["season"]) in acceptable_seasons) and season_data[
            "leagueAbbrev"
        ] == "NHL":
            ppg += season_data["powerPlayGoals"]
            games += season_data["gamesPlayed"]

    return ppg / games if games != 0 else 0.0


def get_five_gpg(data):
    goals = 0
    games = 5

    try:
        for game_data in data["last5Games"]:
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
