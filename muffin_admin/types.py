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
