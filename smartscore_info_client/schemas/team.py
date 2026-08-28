from marshmallow import Schema, fields

# Fields dropped when a team entry is merged into the pipeline payload.
TEAM_MERGE_EXCLUDED_FIELDS = ("team_id", "opponent_id", "season", "team_abbr")


class TeamInfoSchema(Schema):
    team_name = fields.Str()
    team_abbr = fields.Str()
    season = fields.Str()
    team_id = fields.Int()
    opponent_id = fields.Int()
    home = fields.Bool()
    tgpg = fields.Float()
    otga = fields.Float()
    otshga = fields.Float()


TEAM_INFO_SCHEMA = TeamInfoSchema()
