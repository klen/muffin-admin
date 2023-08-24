"""Custom types."""

from typing import Any, Callable, Dict, Tuple, TypedDict

from marshmallow.fields import Field
from typing_extensions import NotRequired, TypeAlias

TRAProps = Dict[str, Any]
TRAInfo = Tuple[str, TRAProps]
TRAConverter = Callable[[Field], TRAInfo]
TRAFields: TypeAlias = Tuple[Tuple[str, TRAInfo], ...]
TRAInputs: TypeAlias = Tuple[Tuple[str, TRAInfo], ...]


class TRAReference(TypedDict):
    key: NotRequired[str]
    source: NotRequired[str]
    reference: NotRequired[str]
    searchKey: NotRequired[str]


TRARefs = Tuple[Tuple[str, TRAReference], ...]


class TRAActionLink(TypedDict):
    label: str
    icon: NotRequired[str]
    title: NotRequired[str]
    field: NotRequired[str]


TRALinks = Tuple[Tuple[str, TRAActionLink], ...]
