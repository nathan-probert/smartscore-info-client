from marshmallow import Schema, fields, post_dump

# Fields dropped when a player entry is merged into the pipeline payload.
PLAYER_MERGE_EXCLUDED_FIELDS = ("team_id", "odds", "stat")


class PlayerInfoSchema(Schema):
    name = fields.Str()
    id = fields.Int()
    team_id = fields.Int()
    gpg = fields.Float()
    hgpg = fields.Float()
    five_gpg = fields.Float()
    hppg = fields.Float()

    @post_dump
    def remove_none_values(self, data, **kwargs):
        return {key: value for key, value in data.items() if value is not None}


PLAYER_INFO_SCHEMA = PlayerInfoSchema()
