"""Custom types."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    NotRequired,
    Protocol,
    TypeAlias,
    TypedDict,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable

    from http_router.types import THostsArg, TMethods

TActionView = Literal["show", "edit", "list", "bulk"]
TRAProps = dict[str, Any]
TRAInfo = tuple[str, TRAProps]
TRAConverter = Callable[[Any], TRAInfo]  # field type depends on the converter
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
    filter: NotRequired[str]


TRALinks = tuple[tuple[str, TRAActionLink], ...]


class TRActionMethod(Protocol):
    """A handler method decorated by `AdminHandler.action`."""

    __action__: dict[str, Any]
    __route__: tuple[tuple[str, ...], TMethods | None, THostsArg | None]

    def __call__(self, *args: Any, **kwargs: Any) -> Awaitable[Any]: ...
