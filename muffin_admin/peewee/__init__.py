"""Peewee ORM Support."""

import typing as t


import peewee as pw
import marshmallow as ma
from muffin_peewee import JSONField
from muffin_rest.peewee import PWRESTBase, PWRESTOptions, PWFilter, Filter

from ..handler import AdminHandler, AdminOptions
from ..typing import RA_INFO


class PWAdminOptions(AdminOptions, PWRESTOptions):

    """Keep PWAdmin options."""

    def setup(self, cls):
        """Auto insert filter by id."""
        super(PWAdminOptions, self).setup(cls)

        for f in self.filters:
            if isinstance(f, Filter):
                f = f.name

            if f == 'id':
                break

        else:
            self.filters = [PWFilter('id', pw_field=self.model_pk), *self.filters]


class PWAdminHandler(AdminHandler, PWRESTBase):

    """Work with Peewee Models."""

    meta_class: t.Type[PWAdminOptions] = PWAdminOptions
    meta: PWAdminOptions

    class Meta:

        """Mark the class as abc base."""

        abc = True

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA inputs."""
        model_field = getattr(cls.meta.model, field.attribute or source, None)
        ra_type, props = super(PWAdminHandler, cls).to_ra_input(field, source)
        if model_field:
            if model_field.choices:
                return 'SelectInput', dict(props, choices=[{
                    "id": c[0], "name": c[1]} for c in model_field.choices])

            if isinstance(model_field, pw.TextField):
                return 'TextInput', dict(props, multiline=True)

            if isinstance(model_field, JSONField) or model_field.field_type.lower() == 'json':
                return 'JsonInput', props

        return ra_type, props

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA fields."""
        model_field = getattr(cls.meta.model, field.attribute or source, None)
        if model_field and \
                (isinstance(model_field, JSONField) or model_field.field_type.lower() == 'json'):
            return 'JsonField', {}

        return super(PWAdminHandler, cls).to_ra_field(field, source)


class PWSearchFilter(PWFilter):

    """Search in query by value."""

    def query(self, query: pw.Query, column: pw.Field, *ops: t.Tuple, **kwargs) -> pw.Query:
        """Apply the filters to Peewee QuerySet.."""
        _, value = ops[0]
        return query.where(column.contains(value))
