"""Peewee ORM Support."""

import typing as t


import peewee as pw
import marshmallow as ma
from muffin_peewee import JSONField
from muffin_rest.peewee import PWRESTBase, PWRESTOptions
from muffin_rest.peewee.filters import PWFilter

from ..handler import AdminHandler, AdminOptions
from ..typing import RA_INFO


class PWAdminOptions(AdminOptions, PWRESTOptions):

    """Keep PWAdmin options."""

    def setup(self, cls):
        """Auto insert filter by id."""
        super(PWAdminOptions, self).setup(cls)

        for flt in self.filters:
            name = flt

            if isinstance(flt, PWFilter):
                name = flt.name

            elif isinstance(flt, tuple):
                name = flt[0]

            if name == 'id':
                break

        else:
            self.filters = [PWFilter('id', field=self.model_pk), *self.filters]


class PWAdminHandler(AdminHandler, PWRESTBase):

    """Work with Peewee Models."""

    meta_class: t.Type[PWAdminOptions] = PWAdminOptions
    meta: PWAdminOptions

    class Meta:

        """Mark the class as abc base."""

        abc = True

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA fields."""
        model_field = getattr(cls.meta.model, field.attribute or source, None)
        if model_field and \
                (isinstance(model_field, JSONField) or model_field.field_type.lower() == 'json'):
            return 'JsonField', {}

        return super(PWAdminHandler, cls).to_ra_field(field, source)

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

            if isinstance(model_field, pw.ForeignKeyField):
                ref = model_field.rel_model._meta.table_name
                if ref in cls.meta.references:
                    props = dict(
                        props, reference=ref, allowEmpty=model_field.null,
                        refProp=cls.meta.references[ref],
                        refSource=model_field.rel_field.name,
                    )
                    return 'FKInput', dict(
                        props, reference=ref, allowEmpty=model_field.null,
                        refProp=cls.meta.references[ref],
                        refSource=model_field.rel_field.name,
                    )

        return ra_type, props


class PWSearchFilter(PWFilter):

    """Search in query by value."""

    def query(self, query: pw.Query, column: pw.Field, *ops: t.Tuple, **kwargs) -> pw.Query:
        """Apply the filters to Peewee QuerySet.."""
        _, value = ops[0]
        return query.where(column.contains(value))
