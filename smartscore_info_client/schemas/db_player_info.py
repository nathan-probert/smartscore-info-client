import ctypes
from dataclasses import dataclass

from marshmallow import Schema, fields


class PlayerDbInfoC(ctypes.Structure):
    _fields_ = [
        ("date", ctypes.c_char_p),
        ("name", ctypes.c_char_p),
        ("gpg", ctypes.c_float),
        ("hgpg", ctypes.c_float),
        ("five_gpg", ctypes.c_float),
        ("tgpg", ctypes.c_float),
        ("otga", ctypes.c_float),
    ]


@dataclass(frozen=True)
class PlayerDbInfo:
    _id: str

    date: str

    name: str
    id: int
    gpg: float
    hgpg: float
    five_gpg: float

    team_name: str
    tgpg: float
    otga: float

    scored: int


class PlayerDbInfoSchema(Schema):
    _id = fields.Str()

    date = fields.Str()

    name = fields.Str()
    id = fields.Int()
    gpg = fields.Float()
    hgpg = fields.Float()
    five_gpg = fields.Float()

    team_name = fields.Str()
    tgpg = fields.Float()
    otga = fields.Float()

    scored = fields.Int()


PLAYER_DB_INFO_SCHEMA = PlayerDbInfoSchema()
