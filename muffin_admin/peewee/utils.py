from peewee import CompositeKey, Field

SEPARATOR = "::"


def composite_key_to_id(fields: list[Field], instance, _) -> str:
    """Convert composite key to string id."""
    return SEPARATOR.join(str(field.db_value(getattr(instance, field.name))) for field in fields)


def id_to_composite_keys(pk: CompositeKey, id_: str) -> dict[str, str]:
    """Convert string id to composite key."""
    values = id_.split(SEPARATOR)
    if len(values) != len(pk.field_names):
        raise ValueError("Invalid id")
    return dict(zip(pk.field_names, values, strict=True))
