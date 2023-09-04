"""Basic admin handler."""

from __future__ import annotations

import inspect
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

import marshmallow as ma
from muffin_rest.handler import RESTBase
from muffin_rest.options import RESTOptions

if TYPE_CHECKING:
    from http_router.types import TMethods

    from muffin_admin.types import TRAFields, TRAInputs, TRALinks, TRARefs

    from .types import TRAConverter, TRAInfo


class AdminOptions(RESTOptions):
    """Prepare admin handler."""

    limit: int = 25
    limit_max: int = 100

    icon: str = ""
    label: str = ""

    create: bool = True
    delete: bool = True
    edit: bool = True
    show: bool = True

    actions: Sequence = ()
    columns: Tuple[str, ...] = ()

    ra_fields: TRAFields = ()
    ra_inputs: TRAInputs = ()
    ra_refs: TRARefs = ()
    ra_links: TRALinks = ()

    def setup(self, cls: AdminHandler):
        """Check and build required options."""
        if not self.limit:
            raise ValueError("`AdminHandler.Meta.limit` can't be nullable.")

        super(AdminOptions, self).setup(cls)

        self.actions = [
            method.__action__
            for _, method in inspect.getmembers(cls, lambda m: hasattr(m, "__action__"))
        ]

        if not self.label:
            self.label = cast(str, self.name)

        if not self.columns:
            self.columns = tuple(
                name
                for name, field in self.Schema._declared_fields.items()
                if field
                and not (
                    field.load_only
                    or name in self.Schema.opts.load_only
                    or name in self.Schema.opts.exclude
                )
            )

        if not self.sorting and self.columns:
            sorting: List[Union[str, Tuple]] = list(self.columns)
            sorting[0] = (sorting[0], {"default": "desc"})
            self.sorting = sorting  # type: ignore[assignment]


class AdminHandler(RESTBase):
    """Basic handler class for admin UI."""

    meta_class: Type[AdminOptions] = AdminOptions
    meta: AdminOptions

    @classmethod
    def action(  # noqa: PLR0913
        cls,
        path: str,
        *,
        methods: Optional[TMethods] = None,
        icon: Optional[str] = None,
        label: Optional[str] = None,
        view: str = "list",
    ):
        """Register an action for the handler.

        Decorate any function to use it as an action.

        :param path: Path to the action
        :param icon: Icon name
        :param label: Label for the action
        :param view: View name (list, show)
        """

        def decorator(method):
            method.__route__ = (path,), methods
            method.__action__ = {
                "view": view,
                "icon": icon,
                "action": path,
                "title": method.__doc__,
                "label": label or method.__name__,
            }
            return method

        return decorator

    @classmethod
    def to_ra(cls) -> Dict[str, Any]:
        """Get JSON params for react-admin."""
        schema_cls = cls.meta.Schema
        schema_opts = schema_cls.opts
        schema_fields = schema_opts.fields
        schema_exclude = schema_opts.exclude
        schema_load_only = schema_opts.load_only
        schema_dump_only = schema_opts.dump_only

        fields_customize = dict(cls.meta.ra_fields)
        inputs_customize = dict(cls.meta.ra_inputs)

        fields = []
        inputs = []

        if not schema_fields:
            schema_fields = list(schema_cls._declared_fields.keys())

        for name in schema_fields:
            field = schema_cls._declared_fields.get(name)

            if not field or name in schema_exclude:
                continue

            source = field.data_key or name
            if not field.load_only and name not in schema_load_only:
                field_info = (
                    fields_customize[source]
                    if source in fields_customize
                    else cls.to_ra_field(field, source)
                )
                if isinstance(field_info, str):
                    field_info = field_info, {}

                field_info[1].setdefault("source", source)
                fields.append(field_info)

            if not field.dump_only and name not in schema_dump_only:
                input_info = (
                    inputs_customize[source]
                    if source in inputs_customize
                    else cls.to_ra_input(field, source)
                )
                if isinstance(input_info, str):
                    input_info = input_info, {}

                input_info[1].setdefault("source", source)
                inputs.append(input_info)

        fields_hash = {
            props["source"]: (
                ra_type,
                dict(props, sortable=props["source"] in cls.meta.sorting),
            )
            for (ra_type, props) in fields
        }

        data = {
            "name": cls.meta.name,
            "label": cls.meta.label,
            "icon": cls.meta.icon,
            "list": {
                "limit": cls.meta.limit,
                "limitMax": cls.meta.limit_max,
                "edit": bool(cls.meta.edit),
                "show": bool(cls.meta.show),
                "actions": [action for action in cls.meta.actions if action["view"] == "list"],
                "fields": [fields_hash[name] for name in cls.meta.columns if name in fields_hash],
                "filters": [
                    (ra_type, dict(source=flt.name, **props))
                    for flt, (ra_type, props) in [
                        (flt, cls.to_ra_input(flt.schema_field, flt.name))
                        for flt in cls.meta.filters.mutations.values()
                    ]
                ],
            },
            "show": {
                "actions": [action for action in cls.meta.actions if action["view"] == "show"],
                "links": cls.meta.ra_links,
                "edit": bool(cls.meta.edit),
                "fields": fields,
            },
            "edit": cls.meta.edit and {
                "actions": [action for action in cls.meta.actions if action["view"] == "edit"],
                "inputs": inputs,
            },
            "create": cls.meta.create and inputs,
            "delete": cls.meta.delete,
        }

        default_sort = cls.meta.sorting.default and cls.meta.sorting.default[0]
        if default_sort:
            data["list"]["sort"] = {  # type: ignore  # noqa:
                "field": default_sort.name,
                "order": default_sort.meta["default"].upper(),
            }

        return data

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> TRAInfo:
        """Convert self schema field to ra field."""
        refs = dict(cls.meta.ra_refs)
        if source in refs:
            ref_data = refs[source]
            return "FKField", {
                "refKey": ref_data.get("key") or "id",
                "refSource": ref_data.get("source") or source,
                "reference": ref_data.get("reference") or source,
            }

        converter = find_ra(field, MA_TO_RAF)
        return converter(field)

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, _: str) -> TRAInfo:
        """Convert a field to react-admin."""
        converter = find_ra(field, MA_TO_RAI)
        rtype, props = converter(field)

        if isinstance(field.load_default, (bool, str, int)):
            props.setdefault("defaultValue", field.load_default)

        if field.required:
            props.setdefault("required", True)

        desc = field.metadata.get("description")
        if desc:
            props.setdefault("helperText", desc)

        return rtype, props


MA_TO_RAF: Dict[Type, TRAConverter] = {
    ma.fields.Boolean: lambda _: ("BooleanField", {}),
    ma.fields.Date: lambda _: ("DateField", {}),
    ma.fields.DateTime: lambda _: ("DateField", {"showTime": True}),
    ma.fields.Number: lambda _: ("NumberField", {}),
    ma.fields.Field: lambda _: ("TextField", {}),
    ma.fields.Email: lambda _: ("EmailField", {}),
    ma.fields.Url: lambda _: ("UrlField", {}),
    # Default
    object: lambda _: ("TextField", {}),
}

MA_TO_RAI: Dict[Type, TRAConverter] = {
    ma.fields.Boolean: lambda _: ("BooleanInput", {}),
    ma.fields.Date: lambda _: ("DateInput", {}),
    ma.fields.DateTime: lambda _: ("DateTimeInput", {}),
    ma.fields.Number: lambda _: ("NumberInput", {}),
    ma.fields.Field: lambda _: ("TextInput", {}),
    # Default
    object: lambda _: ("TextField", {}),
}


def find_ra(field: ma.fields.Field, types: Dict[Type, TRAConverter]) -> TRAConverter:
    """Find a converter for first supported field class."""
    for fcls in type(field).mro():
        if fcls in types:
            return types[fcls]

    return types[object]
