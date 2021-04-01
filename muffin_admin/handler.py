"""Basic admin handler."""

import typing as t

import marshmallow as ma
from muffin_rest.handler import RESTBase, RESTOptions


class AdminOptions(RESTOptions):

    """Prepare admin handler."""

    label: str = ''

    def setup(self, cls):
        """Check and build required options."""
        if not self.limit:
            raise ValueError("`AdminHandler.Meta.limit` can't be nullable.")

        super(AdminOptions, self).setup(cls)

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
            self.sorting = {c: True for c in self.columns}


class AdminHandler(RESTBase):

    """Basic handler class for admin UI."""

    meta_class: t.Type[AdminOptions] = AdminOptions

    class Meta:

        """Tune the handler."""

        abc = True

        limit: int = 50

        icon: t.Optional[str] = None
        label: t.Optional[str] = None

        columns: t.Optional[t.List[str]] = None
        references: t.Dict[str, str] = {}

        create: bool = True
        delete: bool = True
        edit: bool = True
        show: bool = True

    @classmethod
    def to_ra(cls):
        """Get JSON params for react-admin."""
        fields = cls.to_ra_fields()
        inputs = cls.to_ra_inputs()
        return {
            "name": cls.meta.name,
            "label": cls.meta.label,
            "icon": cls.meta.icon,
            "list": {
                "perPage": cls.meta.limit,
                "children": [
                    (rtype, props) for rtype, props in fields
                    if props['source'] in cls.meta.columns],
                "filters": [
                    info for info in [cls.to_ra_input(f.field, f.name) for f in cls.meta.filters]
                    if info
                ],
            },
            "show": cls.meta.show and fields,
            "create": cls.meta.create and inputs,
            "edit": cls.meta.edit and inputs,
            "delete": cls.meta.delete,
        }

    @classmethod
    def to_ra_fields(cls):
        """Convert self schema to ra fields."""
        schema = cls.meta.Schema
        ignore = schema.opts.exclude + schema.opts.load_only
        return [info for info in [
            cls.to_ra_field(field, name) for name, field in schema._declared_fields.items()
            if field and not field.load_only and name not in ignore
        ] if info]

    @classmethod
    def to_ra_field(cls, field, name):
        """Convert self schema field to ra field."""
        source = field.data_key or name
        if source in cls.meta.references:
            ref, _, rfield = cls.meta.references[source].partition('.')
            return 'ReferenceField', {
                'children': [('TextField', {'source': rfield or 'id'})],
                'reference': ref, 'link': 'show',
                'source': source,
            }

        converter = find_ra(field, MA_TO_RAF)
        if converter:
            rtype, props = converter(field)
            props['source'] = source
            return rtype, props

    @classmethod
    def to_ra_inputs(cls):
        """Convert fields to react-admin."""
        schema = cls.meta.Schema
        ignore = schema.opts.exclude + schema.opts.dump_only
        return [info for info in [
            cls.to_ra_input(field, name) for name, field in schema._declared_fields.items()
            if field and not field.dump_only and name not in ignore
        ] if info]

    @classmethod
    def to_ra_input(cls, field, name):
        """Convert a field to react-admin."""
        converter = find_ra(field, MA_TO_RAI)
        if converter:
            rtype, props = converter(field)
            props['source'] = field.attribute or name

            if isinstance(field.default, (bool, str, int)):
                props.setdefault('initialValue', field.default)

            if field.required:
                props.setdefault('required', True)

            return rtype, props


MA_TO_RAF = {
    ma.fields.Boolean: lambda f: ['BooleanField', {}],
    ma.fields.Date: lambda f: ['DateField', {}],
    ma.fields.DateTime: lambda f: ['DateField', {'showTime': True}],
    ma.fields.Number: lambda f: ['NumberField', {}],
    ma.fields.Field: lambda f: ['TextField', {}],

    ma.fields.Email: lambda f: ['EmailField', {}],
    ma.fields.Url: lambda f: ['UrlField', {}],
}

MA_TO_RAI = {
    ma.fields.Boolean: lambda f: ['BooleanInput', {}],
    ma.fields.Date: lambda f: ['DateInput', {}],
    ma.fields.DateTime: lambda f: ['DateTimeInput', {}],
    ma.fields.Number: lambda f: ['NumberInput', {}],
    ma.fields.Field: lambda f: ['TextInput', {}],
}


def find_ra(field, types):
    """Find a converter for first supported field class."""
    for fcls in type(field).mro():
        if fcls in types:
            return types[fcls]
