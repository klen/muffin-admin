"""SQLAlchemy core support."""

import typing as t

import marshmallow as ma
from muffin_rest.filters import Filter
from muffin_rest.sqlalchemy import SARESTHandler, SARESTOptions
from muffin_rest.sqlalchemy.filters import SAFilter
from sqlalchemy import JSON, Enum, Text

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

            if f == "id":
                break

        else:
            self.filters = [SAFilter("id", field=self.table_pk), *self.filters]


class SAAdminHandler(AdminHandler, SARESTHandler):

    """Work with SQLAlchemy Core."""

    meta_class: t.Type[SAAdminOptions] = SAAdminOptions
    meta: SAAdminOptions

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA fields."""
        column = getattr(cls.meta.table.c, field.attribute or source, None)
        if column is not None:
            if column.foreign_keys:
                fk = list(column.foreign_keys)[0]
                ref = fk.column.table.name
                if ref in cls.meta.references:
                    return "FKField", {
                        "reference": ref,
                        "source": source,
                        "refSource": cls.meta.references[ref],
                    }

            if isinstance(column.type, JSON):
                return "JsonField", {}

        return super(SAAdminHandler, cls).to_ra_field(field, source)

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA inputs."""
        column = getattr(cls.meta.table.c, field.attribute or source, None)
        ra_type, props = super(SAAdminHandler, cls).to_ra_input(field, source)
        if column is not None:
            if column.foreign_keys and (source in cls.meta.references):
                ref, _, ref_source = cls.meta.references[source].partition(".")
                fk = list(column.foreign_keys)[0]
                return "FKInput", dict(
                    props,
                    emptyValue=None if column.nullable else "",
                    refSource=fk.column.name,
                    refProp=ref_source or ref,
                    reference=ref_source and ref or fk.column.table.name,
                )

            if isinstance(column.type, Enum):
                return "SelectInput", dict(
                    props,
                    choices=[
                        {"id": c.value, "name": c.name} for c in column.type.enum_class
                    ],
                )

            if isinstance(column.type, Text):
                return "TextInput", dict(props, multiline=True)

            if isinstance(column.type, JSON):
                return "JsonInput", props

        return ra_type, props
