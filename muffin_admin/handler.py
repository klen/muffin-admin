"""Basic admin handler."""

from __future__ import annotations

import typing as t
import inspect

import marshmallow as ma
from muffin_rest.handler import RESTBase, RESTOptions

from .typing import RA_INFO, RA_CONVERTER


class AdminOptions(RESTOptions):

    """Prepare admin handler."""

    limit: int = 25
    limit_max: int = 100

    icon: str = ''
    label: str = ''

    create: bool = True
    delete: bool = True
    edit: bool = True
    show: bool = True

    columns: t.List[str] = []
    references: t.Dict[str, str] = {}
    actions: t.Sequence = ()

    ra_fields: t.Dict[str, RA_INFO] = {}
    ra_inputs: t.Dict[str, RA_INFO] = {}

    def setup(self, cls: AdminHandler):
        """Check and build required options."""
        if not self.limit:
            raise ValueError("`AdminHandler.Meta.limit` can't be nullable.")

        super(AdminOptions, self).setup(cls)

        self.actions = [
            method.__action__
            for _, method in inspect.getmembers(cls, lambda m: hasattr(m, '__action__'))
        ]

        if not self.label:
            self.label = self.name

        if not self.columns:
            self.columns = [
                name for name, field in self.Schema._declared_fields.items()
                if field and not (
                    field.load_only or
                    name in self.Schema.opts.load_only or
                    name in self.Schema.opts.exclude)
            ]

        if not self.sorting and self.columns:
            self.sorting = [name for name in self.columns]
            self.sorting[0] = (self.sorting[0], {'default': 'desc'})


class AdminHandler(RESTBase):

    """Basic handler class for admin UI."""

    meta_class: t.Type[AdminOptions] = AdminOptions
    meta: AdminOptions

    class Meta:

        """Tune the handler."""

        abc: bool = True

    @classmethod
    def action(
            cls, path: str, *, icon: str = None, label: str = None, view: str = 'list', **params):
        """Decorate any function as an action."""
        def decorator(method):
            method.__route__ = (path,), params
            method.__action__ = {
                'view': view,
                'icon': icon,
                'action': path,
                'title': method.__doc__,
                'label': label or method.__name__,
            }
            return method

        return decorator

    @classmethod
    def to_ra(cls) -> t.Dict[str, t.Any]:
        """Get JSON params for react-admin."""
        Schema = cls.meta.Schema
        exclude = Schema.opts.exclude
        load_only = Schema.opts.load_only
        dump_only = Schema.opts.dump_only
        fields_customize = cls.meta.ra_fields
        inputs_customize = cls.meta.ra_inputs
        fields = []
        inputs = []
        for name, field in Schema._declared_fields.items():
            if not field or name in exclude:
                continue

            source = field.data_key or name
            if not field.load_only and name not in load_only:
                field_info = fields_customize[source] if source in fields_customize else cls.to_ra_field(field, source)  # noqa
                field_info[1].setdefault('source', source)
                fields.append(field_info)
            if not field.dump_only and name not in dump_only:
                input_info = inputs_customize[source] if source in inputs_customize else cls.to_ra_input(field, source)  # noqa
                input_info[1].setdefault('source', source)
                inputs.append(input_info)

        fields_hash = {props['source']: (
            ra_type, dict(props, sortable=props['source'] in cls.meta.sorting))
            for (ra_type, props) in fields}

        data = {
            "name": cls.meta.name,
            "label": cls.meta.label,
            "icon": cls.meta.icon,
            "list": {
                "limit": cls.meta.limit,
                "limitMax": cls.meta.limit_max,
                "edit": bool(cls.meta.edit),
                "show": bool(cls.meta.show),
                "actions": [action for action in cls.meta.actions if action['view'] == 'list'],
                "children": [
                    fields_hash[name] for name in cls.meta.columns if name in fields_hash],
                "filters": [
                    (ra_type, dict(source=flt.name, **props))
                    for flt, (ra_type, props) in [
                        (flt, cls.to_ra_input(flt.schema_field, flt.name))
                        for flt in cls.meta.filters.mutations.values()
                    ]
                ],
            },
            "show": {
                "actions": [action for action in cls.meta.actions if action['view'] == 'show'],
                "fields": fields,
            },
            "edit": {
                "actions": [action for action in cls.meta.actions if action['view'] == 'edit'],
                "inputs": inputs,
            },
            "create": cls.meta.create and inputs,
            "delete": cls.meta.delete,
        }

        default_sort = cls.meta.sorting.default and cls.meta.sorting.default[0]
        if default_sort:
            data['list']['sort'] = {
                'field': default_sort.name,
                'order': default_sort.meta['default'].upper(),
            }

        return data

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Convert self schema field to ra field."""
        if source in cls.meta.references:
            return 'FKField', {'reference': source, 'refSource': cls.meta.references[source]}

        converter = find_ra(field, MA_TO_RAF)
        return converter(field)

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Convert a field to react-admin."""
        converter = find_ra(field, MA_TO_RAI)
        rtype, props = converter(field)

        if isinstance(field.default, (bool, str, int)):
            props.setdefault('initialValue', field.default)

        if field.required:
            props.setdefault('required', True)

        return rtype, props


MA_TO_RAF: t.Dict[type, RA_CONVERTER] = {
    ma.fields.Boolean: lambda f: ('BooleanField', {}),
    ma.fields.Date: lambda f: ('DateField', {}),
    ma.fields.DateTime: lambda f: ('DateField', {'showTime': True}),
    ma.fields.Number: lambda f: ('NumberField', {}),
    ma.fields.Field: lambda f: ('TextField', {}),

    ma.fields.Email: lambda f: ('EmailField', {}),
    ma.fields.Url: lambda f: ('UrlField', {}),

    # Default
    object: lambda f: ('TextField', {}),
}

MA_TO_RAI: t.Dict[type, RA_CONVERTER] = {
    ma.fields.Boolean: lambda f: ('BooleanInput', {}),
    ma.fields.Date: lambda f: ('DateInput', {}),
    ma.fields.DateTime: lambda f: ('DateTimeInput', {}),
    ma.fields.Number: lambda f: ('NumberInput', {}),
    ma.fields.Field: lambda f: ('TextInput', {}),

    # Default
    object: lambda f: ('TextField', {}),
}


def find_ra(field: ma.fields.Field, types: t.Dict[type, RA_CONVERTER]) -> RA_CONVERTER:
    """Find a converter for first supported field class."""
    for fcls in type(field).mro():
        if fcls in types:
            return types[fcls]

    return types[object]
