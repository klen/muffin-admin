"""Custom types."""

from typing import Any, Callable, Dict, Tuple, TypedDict

from marshmallow.fields import Field
from typing_extensions import NotRequired

TRAProps = Dict[str, Any]
TRAInfo = Tuple[str, TRAProps]
TRAConverter = Callable[[Field], TRAInfo]


class TRAActionLink(TypedDict):
    label: str
    icon: NotRequired[str]
    title: NotRequired[str]
    field: NotRequired[str]


class TRAReference(TypedDict):
    key: NotRequired[str]
    source: NotRequired[str]
    reference: NotRequired[str]
    searchKey: NotRequired[str]
