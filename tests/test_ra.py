from enum import Enum

import marshmallow as ma

from muffin_admin.handler import AdminHandler


def test_ma_enum_to_ra():
    class TestEnum(Enum):
        a = "a"
        b = "b"
        c = "c"

    res = AdminHandler.to_ra_input(ma.fields.Enum(TestEnum), source="test")
    assert res == (
        "SelectArrayInput",
        {
            "choices": [
                {"id": "a", "name": "a"},
                {"id": "b", "name": "b"},
                {"id": "c", "name": "c"},
            ]
        },
    )
