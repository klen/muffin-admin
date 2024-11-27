"""Custom types."""

from typing import Any, Callable, Literal, TypedDict

from marshmallow.fields import Field

try:
    from typing import NotRequired, TypeAlias  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import NotRequired, TypeAlias

TActionView = Literal["show", "edit", "list", "bulk"]
TRAProps = dict[str, Any]
TRAInfo = tuple[str, TRAProps]
TRAConverter = Callable[[Field], TRAInfo]
TRAInputs: TypeAlias = tuple[tuple[str, TRAInfo], ...]


class TRAReference(TypedDict):
    key: NotRequired[str]
    source: NotRequired[str]
    reference: NotRequired[str]
    searchKey: NotRequired[str]


class TRAActionLink(TypedDict):
    label: NotRequired[str]
    icon: NotRequired[str]
    title: NotRequired[str]
    field: NotRequired[str]


TRALinks = tuple[tuple[str, TRAActionLink], ...]
