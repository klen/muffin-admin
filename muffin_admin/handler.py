"""Basic admin handler."""

from __future__ import annotations

import inspect
from functools import wraps
from typing import TYPE_CHECKING, Any, ClassVar, Iterable, Optional, Sequence, Union, cast

import marshmallow as ma
from muffin_rest import APIError
from muffin_rest.handler import RESTBase
from muffin_rest.options import RESTOptions
from muffin_rest.schemas import EnumField

from muffin_admin.types import TActionView, TRAInputs, TRALinks, TRAReference

if TYPE_CHECKING:
    from http_router.types import TMethods
    from muffin import Request, Response
    from muffin_rest.filters import Filter

    from .types import TRAConverter, TRAInfo


class AdminOptions(RESTOptions):
    """Prepare admin handler."""

    limit: int = 25
    limit_max: int = 100
    limit_total = False

    icon: str = ""
    label: str = ""

    create: bool = True
    delete: bool = True
    edit: bool = True
    show: bool = True

    actions: Sequence = ()
    columns: tuple[str, ...] = ()
    help: Optional[str] = None
    locales: Optional[dict[str, dict[str, Any]]] = None

    ra_order: int = 0
    ra_fields: ClassVar[dict[str, TRAInfo]] = {}
    ra_inputs: ClassVar[dict[str, TRAInfo]] = {}
    ra_filters: ClassVar[dict[str, TRAInfo]] = {}
    ra_refs: ClassVar[dict[str, TRAReference]] = {}
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
            self.default_sort()

    def default_sort(self):
        """Get default sorting."""
        sorting: list[Union[str, tuple]] = list(self.columns)
        sorting[0] = (sorting[0], {"default": "desc"})
        self.sorting = sorting  # type: ignore[assignment]


class AdminHandler(RESTBase):
    """Basic handler class for admin UI."""

    meta_class: type[AdminOptions] = AdminOptions
    meta: AdminOptions

    async def __call__(self, request: Request, *, method_name=None, **_):
        """Handle the request."""
        response = await super(AdminHandler, self).__call__(request, method_name=method_name)
        await self.log(request, response, method_name)
        return response

    async def log(self, request: Request, response: Optional[Response], action: Optional[str]):
        """Log the request."""

    def get_selected(self, request: Request) -> Optional[Iterable]:
        """Get selected objects."""
        ids = request.query.getall("ids", None)
        return ids

    @classmethod
    def action(
        cls,
        *paths: str,
        methods: Optional[TMethods] = None,
        icon: Optional[str] = None,
        label: Optional[str] = None,
        view: Optional[list[TActionView] | TActionView] = None,
        schema: Optional[type[ma.Schema]] = None,
        **opts,
    ):
        """Register an action for the handler.

        Decorate any function to use it as an action.

        :param path: Path to the action
        :param icon: Icon name
        :param label: Label for the action
        :param view: View name (list, show)
        """

        def decorator(method):
            if schema is None:
                wrapper = method
            else:

                @wraps(method)
                async def wrapper(self, request: Request, **kwargs):
                    try:
                        raw_data = cast(dict, await request.json())
                        data = schema().load(raw_data)  # type: ignore[]
                    except ValueError:
                        raise APIError.BAD_REQUEST("Invalid data") from None
                    except ma.ValidationError as exc:
                        raise APIError.BAD_REQUEST("Invalid data", errors=exc.messages) from None

                    return await method(self, request, data=data, **kwargs)

            wrapper.__route__ = paths, methods  # type: ignore[]
            wrapper.__action__ = {  # type: ignore[]
                "view": [view] if isinstance(view, str) else view,
                "icon": icon,
                "paths": paths,
                "title": method.__doc__,
                "id": method.__name__,
                "label": label or " ".join(method.__name__.split("_")).capitalize(),
                **opts,
            }

            if schema:
                wrapper.__action__["schema"] = schema  # type: ignore[]

            return wrapper

        return decorator

    @classmethod
    def to_ra(cls) -> dict[str, Any]:
        """Get JSON params for react-admin."""
        meta = cls.meta

        actions = []
        for source in meta.actions:
            info = dict(source)
            if info.get("schema"):
                _, inputs = cls.to_ra_schema(info["schema"], resource=False)
                info["schema"] = inputs
            actions.append(info)

        fields, inputs = cls.to_ra_schema(meta.Schema)  # type: ignore[]
        fields_hash = {
            props["source"]: (ra_type, dict(props, sortable=props["source"] in meta.sorting))
            for (ra_type, props) in fields
        }

        data = {
            "name": meta.name,
            "label": meta.label,
            "icon": meta.icon,
            "help": meta.help,
            "actions": actions,
            "list": {
                "create": meta.create,
                "remove": bool(meta.delete),
                "edit": bool(meta.edit),
                "limit": meta.limit,
                "limitMax": meta.limit_max,
                "limitTotal": meta.limit_total,
                "show": bool(meta.show),
                "fields": [fields_hash[name] for name in meta.columns if name in fields_hash],
                "filters": [cls.to_ra_filter(flt) for flt in meta.filters.mutations.values()],
            },
            "show": {
                "links": meta.ra_links,
                "edit": bool(meta.edit),
                "fields": fields,
            },
            "create": meta.create and inputs,
            "edit": meta.edit
            and {
                "inputs": inputs,
                "remove": meta.delete,
            },
            "delete": meta.delete,
        }

        default_sort = meta.sorting.default and meta.sorting.default[0]
        if default_sort:
            data["list"]["sort"] = {  # type: ignore[call-overload, index]
                "field": default_sort.name,
                "order": default_sort.meta["default"].upper(),
            }

        return data

    @classmethod
    def to_ra_schema(cls, schema_cls: type[ma.Schema], *, resource: bool = True):
        meta = cls.meta
        schema_opts = schema_cls.opts
        schema_fields = schema_opts.fields
        schema_exclude = schema_opts.exclude
        schema_load_only = schema_opts.load_only
        schema_dump_only = schema_opts.dump_only

        fields_customize = meta.ra_fields
        inputs_customize = meta.ra_inputs
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
                    else cls.to_ra_input(field, source, resource=resource)
                )
                if isinstance(input_info, str):
                    input_info = input_info, {}

                input_info[1].setdefault("source", source)
                inputs.append(input_info)

        return cast(TRAInputs, fields), cast(TRAInputs, inputs)

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> TRAInfo:
        """Convert self schema field to ra field."""
        refs = cls.meta.ra_refs
        if source in refs:
            ref_data = refs[source]
            return "FKField", {
                "refKey": ref_data.get("key") or "id",
                "refSource": ref_data.get("source") or source,
                "reference": ref_data.get("reference") or source,
            }

        return ma_to_ra(field, MA_TO_RAF)

    @classmethod
    def to_ra_filter(cls, flt: Filter) -> TRAInfo:
        custom = cls.meta.ra_filters

        if flt.name in custom:
            ra_type, props = custom[flt.name]

        elif isinstance(flt.schema_field, ma.fields.Enum):
            return "SelectArrayInput", {
                "source": flt.name,
                "choices": [{"id": c.value, "name": c.name} for c in flt.schema_field.enum],
            }
        else:
            ra_type, props = cls.to_ra_input(flt.schema_field, flt.name, resource=True)

        props["source"] = flt.name
        return ra_type, props

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str, *, resource: bool = True) -> TRAInfo:
        """Convert a field to react-admin."""
        rtype, props = ma_to_ra(field, MA_TO_RAI)

        if isinstance(field.load_default, (bool, str, int)):
            props.setdefault("defaultValue", field.load_default)

        if field.required:
            props.setdefault("required", True)

        metadata = field.metadata
        desc = metadata.get("description")
        if desc:
            props.setdefault("helperText", desc)

        label = metadata.get("label")
        if label:
            props.setdefault("label", label)

        return rtype, props


MA_TO_RAF: dict[type, TRAConverter] = {
    ma.fields.Boolean: lambda _: ("BooleanField", {}),
    ma.fields.Date: lambda _: ("DateField", {}),
    ma.fields.DateTime: lambda _: ("DateField", {"showTime": True}),
    ma.fields.Number: lambda _: ("NumberField", {}),
    ma.fields.Field: lambda _: ("TextField", {}),
    ma.fields.Email: lambda _: ("EmailField", {}),
    ma.fields.Url: lambda _: ("UrlField", {}),
    ma.fields.Enum: lambda field: (
        "SelectField",
        {"choices": [{"id": choice.value, "name": choice.name} for choice in field.enum]},  # type: ignore[attr-defined]
    ),
    # Default
    object: lambda _: ("TextField", {}),
}

MA_TO_RAI: dict[type, TRAConverter] = {
    ma.fields.Boolean: lambda _: ("BooleanInput", {}),
    ma.fields.Date: lambda _: ("DateInput", {}),
    ma.fields.DateTime: lambda _: ("DateTimeInput", {}),
    ma.fields.Number: lambda _: ("NumberInput", {}),
    ma.fields.Field: lambda _: ("TextInput", {}),
    ma.fields.Enum: lambda field: (
        "SelectInput",
        {"choices": [{"id": choice.value, "name": choice.name} for choice in field.enum]},  # type: ignore[attr-defined]
    ),
    # Default
    object: lambda _: ("TextField", {}),
}

# Support EnumField from muffin-rest
MA_TO_RAI[EnumField] = MA_TO_RAI[ma.fields.Enum]


def ma_to_ra(field: ma.fields.Field, types: dict[type, TRAConverter]) -> TRAInfo:
    """Convert a field to fa."""
    converter = types[object]
    for fcls in type(field).mro():
        if fcls in types:
            converter = types[fcls]
            break

    return converter(field)
