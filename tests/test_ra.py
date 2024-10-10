from enum import StrEnum

import marshmallow as ma

from muffin_admin.handler import AdminHandler


def test_ma_enum_to_ra():
    class TestEnum(StrEnum):
        a = "a"
        b = "b"
        c = "c"

    res = AdminHandler.to_ra_input(ma.fields.Enum(TestEnum), source="test")
    assert res == (
        "SelectInput",
        {
            "choices": [
                {"id": "a", "name": "a"},
                {"id": "b", "name": "b"},
                {"id": "c", "name": "c"},
            ]
        },
    )
