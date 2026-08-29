"""Client for the NHL's public APIs, returning parsed models."""

from ..models.player import PlayerStats
from ..models.team import TeamStats
from ..utility import exponential_backoff_request

SCHEDULE_URL = "https://api-web.nhle.com/v1/schedule/{date}"
SCORE_URL = "https://api-web.nhle.com/v1/score/{date}"
ROSTER_URL = "https://api-web.nhle.com/v1/roster/{team_abbr}/current"
PLAYER_LANDING_URL = "https://api-web.nhle.com/v1/player/{player_id}/landing"
TEAM_SUMMARY_URL = (
    "https://api.nhle.com/stats/rest/en/team/summary"
    "?cayenneExp=seasonId={season}%20and%20gameTypeId=2"
)
TEAM_PENALTY_KILL_URL = (
    "https://api.nhle.com/stats/rest/en/team/penaltykilltime"
    "?cayenneExp=seasonId={season}%20and%20gameTypeId=2"
)


class NHLClient:
    """Parses NHL API responses into models with a per-season payload cache."""

    def __init__(self):
        self._team_summary = {}
        self._team_penalty_kill = {}

    def get_schedule(self, date):
        return exponential_backoff_request(SCHEDULE_URL.format(date=date))

    def get_score(self, date):
        return exponential_backoff_request(SCORE_URL.format(date=date))

    def get_roster(self, team_abbr):
        return exponential_backoff_request(ROSTER_URL.format(team_abbr=team_abbr))

    def get_player_landing(self, player_id):
        return exponential_backoff_request(
            PLAYER_LANDING_URL.format(player_id=player_id)
        )

    def get_player_stats(self, player_id, years=3) -> PlayerStats:
        return PlayerStats.from_landing_payload(
            self.get_player_landing(player_id), years=years
        )

    def get_team_summary(self, season):
        if season not in self._team_summary:
            self._team_summary[season] = exponential_backoff_request(
                TEAM_SUMMARY_URL.format(season=season)
            )
        return self._team_summary[season]

    def get_team_penalty_kill(self, season):
        if season not in self._team_penalty_kill:
            self._team_penalty_kill[season] = exponential_backoff_request(
                TEAM_PENALTY_KILL_URL.format(season=season)
            )
        return self._team_penalty_kill[season]

    def get_team_stats(self, season, team_id, opponent_id) -> TeamStats:
        return TeamStats.from_payloads(
            self.get_team_summary(season),
            self.get_team_penalty_kill(season),
            team_id,
            opponent_id,
        )
