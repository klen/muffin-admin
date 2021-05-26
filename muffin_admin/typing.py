"""Custom types."""

from typing import Any, Callable, Dict, Tuple

from marshmallow.fields import Field

RA_PROPS = Dict[str, Any]
RA_INFO = Tuple[str, RA_PROPS]
RA_CONVERTER = Callable[[Field], RA_INFO]
