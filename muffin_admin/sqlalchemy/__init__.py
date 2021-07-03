"""SQLAlchemy core support."""

import typing as t

import marshmallow as ma
from muffin_rest.sqlalchemy import SARESTOptions, SARESTHandler
from muffin_rest.sqlalchemy.filters import SAFilter, Filter
from sqlalchemy import Enum, Text, JSON

from ..handler import AdminHandler, AdminOptions
from ..typing import RA_INFO


class SAAdminOptions(AdminOptions, SARESTOptions):

    """Keep SAAdmin options."""

    def setup(self, cls):
        """Auto insert filter by id."""
        super(SAAdminOptions, self).setup(cls)

        for f in self.filters:
            if isinstance(f, Filter):
                f = f.name

            if f == 'id':
                break

        else:
            self.filters = [SAFilter('id', field=self.table_pk), *self.filters]


class SAAdminHandler(AdminHandler, SARESTHandler):

    """Work with SQLAlchemy Core."""

    meta_class: t.Type[SAAdminOptions] = SAAdminOptions
    meta: SAAdminOptions

    class Meta:

        """Mark the class as abc base."""

        abc = True

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA fields."""
        column = getattr(cls.meta.table.c, field.attribute or source, None)
        if column is not None:
            if column.foreign_keys:
                fk = list(column.foreign_keys)[0]
                ref = fk.column.table.name
                if ref in cls.meta.references:
                    return 'FKField', {
                        'reference': ref, 'source': source, 'refSource': cls.meta.references[ref]}

            if isinstance(column.type, JSON):
                return 'JsonField', {}

        return super(SAAdminHandler, cls).to_ra_field(field, source)

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA inputs."""
        column = getattr(cls.meta.table.c, field.attribute or source, None)
        ra_type, props = super(SAAdminHandler, cls).to_ra_input(field, source)
        if column is not None:
            if column.foreign_keys:
                fk = list(column.foreign_keys)[0]
                ref = fk.column.table.name
                if ref in cls.meta.references:
                    props = dict(
                        props, reference=ref, allowEmpty=column.nullable,
                        refProp=cls.meta.references[ref], refSource=fk.column.name,
                    )
                    return 'FKInput', props

            if isinstance(column.type, Enum):
                return 'SelectInput', dict(props, choices=[
                    {"id": c.value, "name": c.name} for c in column.type.enum_class
                ])

            if isinstance(column.type, Text):
                return 'TextInput', dict(props, multiline=True)

            if isinstance(column.type, JSON):
                return 'JsonInput', props

        return ra_type, props
