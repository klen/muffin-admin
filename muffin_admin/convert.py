"""Convert marshmallow fields to ra-admin types."""

import marshmallow as ma


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


def convert_fields(fields, types='inputs'):
    """Convert the given fields to the given types."""
    types = MA_TO_RAI if types == 'inputs' else MA_TO_RAF
    for name, field in fields:
        if field:
            for fcls in type(field).mro():
                if fcls in types:
                    ra_type, props = types[fcls](field)
                    props['source'] = name

                    if isinstance(field.default, (bool, str, int)):
                        props.setdefault('initialValue', field.default)

                    if field.required:
                        props.setdefault('required', True)

                    yield (ra_type, props)
                    break
