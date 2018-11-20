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
