"""Support admin filters."""
import wtforms as wtf


PREFIX = 'af-'


class FilterDefault:

    """Default filters value."""

    def __str__(self):
        """Nothing here."""
        return ""

DEFAULT = FilterDefault()


class Filter:

    """Implement admin filters."""

    field = wtf.StringField
    default = DEFAULT
    field_kwargs = {}

    def __init__(self, name, **field_kwargs):
        """Store name and mode."""
        self.name = name
        self.field_kwargs = field_kwargs or self.field_kwargs

    def bind(self, form):
        """Bind to filters form."""
        field = self.field(default=self.default, **self.field_kwargs)
        form._fields[self.name] = field.bind(form, self.name, prefix=form._prefix)

    def value(self, data):
        """Get value from data."""
        value = data.get(self.name, self.default)
        return value or self.default

    def apply(self, collection, data):
        """Filter collection."""
        value = self.value(data)
        if value is self.default:
            return collection
        return [o for o in collection if getattr(o, self.name, None) == value]


class BoolFilter(Filter):

    """Boolean filter."""

    field = wtf.BooleanField


class ChoiceFilter(Filter):

    """Boolean filter."""

    field = wtf.SelectField


def default_converter(handler, flt):
    """Convert column name to filter."""
    if isinstance(flt, Filter):
        return flt
    return Filter(flt)


class PWFilter(Filter):

    """Base filter for Peewee handlers."""

    def apply(self, query, data):
        """Filter a query."""
        field = query.model_class._meta.fields.get(self.name)
        if not field or self.name not in data:
            return query
        value = self.value(data)
        if value is self.default:
            return query
        value = field.db_value(value)
        return self.filter_query(query, field, value)

    @staticmethod
    def filter_query(query, field, value):
        """Filter a query."""
        return query.where(field == value)


class PWLikeFilter(PWFilter):

    """Filter query by value."""

    def filter_query(self, query, field, value):
        """Filter a query."""
        value = "*%s*" % value
        return query.where(field % value)


class PWBoolFilter(PWFilter):

    """Boolean filter."""

    field = wtf.SelectField
    field_kwargs = {
        'choices': (
            (Filter.default, '---'),
            (1, 'yes'),
            (0, 'no'),
        )
    }

    def value(self, data):
        """Get value from data."""
        value = data.get(self.name)
        if value:
            return int(value)
        return self.default


class PWChoiceFilter(PWFilter):

    """Select field."""

    field = wtf.SelectField


def pw_converter(handler, flt):
    """Convert column name to filter."""
    import peewee as pw

    if isinstance(flt, Filter):
        return flt

    model = handler.model
    field = getattr(model, flt)

    if isinstance(field, pw.BooleanField):
        return PWBoolFilter(flt)

    if field.choices:
        choices = [(Filter.default, '---')] + list(field.choices)
        return PWChoiceFilter(flt, choices=choices)

    return PWFilter(flt)
