"""SQLAlchemy core support."""

from __future__ import annotations

from typing import TYPE_CHECKING

from muffin_rest.filters import Filter
from muffin_rest.sqlalchemy import SARESTHandler, SARESTOptions
from muffin_rest.sqlalchemy.filters import SAFilter
from sqlalchemy import JSON, Enum, Text

from muffin_admin.handler import AdminHandler, AdminOptions

if TYPE_CHECKING:
    import marshmallow as ma
    from muffin import Request

    from muffin_admin.types import TRAInfo


class SAAdminOptions(AdminOptions, SARESTOptions):
    """Keep SAAdmin options."""

    def setup(self, cls):
        """Auto insert filter by id."""
        super(SAAdminOptions, self).setup(cls)

        for f in self.filters:
            if f == "id" or (isinstance(f, Filter) and f.name == "id"):
                break

        else:
            self.filters = [SAFilter("id", field=self.table_pk), *self.filters]


class SAAdminHandler(AdminHandler, SARESTHandler):
    """Work with SQLAlchemy Core."""

    meta_class: type[SAAdminOptions] = SAAdminOptions
    meta: SAAdminOptions

    def get_selected(self, request: Request):
        ids = request.query.getall("ids")
        qs = self.collection
        if ids:
            qs = qs.where(self.meta.table_pk.in_(ids))

        return qs

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> TRAInfo:
        """Setup RA fields."""
        column = getattr(cls.meta.table.c, field.attribute or source, None)
        refs = dict(cls.meta.ra_refs)
        if column is not None:
            if column.foreign_keys and column.name in refs:
                ref_data = refs[column.name]
                fk = next(iter(column.foreign_keys))
                return "FKField", {
                    "source": source,
                    "refKey": ref_data.get("key") or fk.column.name,
                    "refSource": ref_data.get("source") or fk.column.name,
                    "reference": ref_data.get("reference") or fk.column.table.name,
                }

            if isinstance(column.type, JSON):
                return "JsonField", {}

        return super(SAAdminHandler, cls).to_ra_field(field, source)

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str, *, resource: bool = True) -> TRAInfo:
        """Setup RA inputs."""
        column = getattr(cls.meta.table.c, field.attribute or source, None)
        ra_type, props = super(SAAdminHandler, cls).to_ra_input(field, source)
        refs = dict(cls.meta.ra_refs)
        if column is not None:
            if column.foreign_keys and (source in refs):
                ref_data = refs[source]
                fk = next(iter(column.foreign_keys))
                return "FKInput", dict(
                    props,
                    emptyValue=None if column.nullable else "",
                    refSource=ref_data.get("source") or fk.column.name,
                    refKey=ref_data.get("key") or fk.column.name,
                    reference=ref_data.get("reference") or fk.column.table.name,
                )

            if isinstance(column.type, Enum):
                return "SelectArrayInput", dict(
                    props,
                    choices=[{"id": c.value, "name": c.name} for c in column.type.enum_class],
                )

            if isinstance(column.type, Text):
                return "TextInput", dict(props, multiline=True)

            if isinstance(column.type, JSON):
                return "JsonInput", props

        return ra_type, props
