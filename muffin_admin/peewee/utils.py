from peewee import CompositeKey

SEPARATOR = "::"


def composite_key_to_id(pk: CompositeKey, instance, _) -> str:
    """Convert composite key to string id."""
    return SEPARATOR.join(str(getattr(instance, field)) for field in pk.field_names)


def id_to_composite_key(pk: CompositeKey, id_: str) -> dict[str, str]:
    """Convert string id to composite key."""
    values = id_.split(SEPARATOR)
    if len(values) != len(pk.field_names):
        raise ValueError("Invalid id")
    return dict(zip(pk.field_names, values, strict=True))
