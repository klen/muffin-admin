"""Peewee ORM Support."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import peewee as pw
from muffin_peewee import JSONLikeField
from muffin_rest.peewee.filters import PWFilter
from muffin_rest.peewee.handler import PWRESTBase
from muffin_rest.peewee.options import PWRESTOptions

from muffin_admin.handler import AdminHandler, AdminOptions

if TYPE_CHECKING:
    import marshmallow as ma
    from muffin import Request
    from muffin_rest.filters import Filter

    from muffin_admin.types import TRAInfo


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

            if name == "id":
                break

        else:
            self.filters = [PWFilter("id", field=self.model_pk), *self.filters]  # type: ignore[]


class PWAdminHandler(AdminHandler, PWRESTBase):
    """Work with Peewee Models."""

    meta_class: type[PWAdminOptions] = PWAdminOptions
    meta: PWAdminOptions

    def get_selected(self, request: Request):
        """Get selected objects."""
        ids = request.query.getall("ids")
        qs = self.collection
        if ids:
            qs = qs.where(self.meta.model_pk.in_(ids))  # type: ignore[]

        return qs

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> TRAInfo:
        """Setup RA fields."""
        model_field = getattr(cls.meta.model, field.attribute or source, None)
        if (
            model_field
            and isinstance(model_field, pw.Field)
            and (isinstance(model_field, JSONLikeField) or model_field.field_type.lower() == "json")
        ):
            return "JsonField", {}

        return super(PWAdminHandler, cls).to_ra_field(field, source)

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str, *, resource: bool = True) -> TRAInfo:
        """Setup RA inputs."""
        model_field = resource and getattr(
            cls.meta.model, field.attribute or field.metadata.get("name") or source, None
        )
        ra_type, props = super(PWAdminHandler, cls).to_ra_input(field, source)
        refs = cls.meta.ra_refs

        if model_field and isinstance(model_field, pw.Field):
            if model_field.choices:
                return "SelectInput", dict(
                    props,
                    choices=[{"id": c[0], "name": c[1]} for c in model_field.choices],
                )

            if isinstance(model_field, pw.TextField):
                return "TextInput", dict(props, multiline=True)

            if isinstance(model_field, JSONLikeField) or model_field.field_type.lower() == "json":
                return "JsonInput", props

            if isinstance(model_field, pw.ForeignKeyField) and source in refs:
                ref_data = refs[source]
                rel_model = model_field.rel_model
                return "FKInput", dict(
                    props,
                    refSource=ref_data.get("source") or model_field.rel_field.name,
                    refKey=ref_data.get("key") or rel_model._meta.primary_key.name,
                    reference=ref_data.get("reference") or rel_model._meta.table_name,
                )

        return ra_type, props

    @classmethod
    def to_ra_filter(cls, flt: Filter) -> TRAInfo:
        field = flt.field
        if field and field.choices:
            return "SelectArrayInput", {
                "source": field.name,
                "choices": [{"id": c[0], "name": c[1]} for c in field.choices],
            }
        return super(PWAdminHandler, cls).to_ra_filter(flt)


class PWSearchFilter(PWFilter):
    """Search in query by value."""

    async def filter(self, collection: pw.ModelSelect, *ops: tuple, **_) -> pw.ModelSelect:
        """Apply the filters to Peewee QuerySet.."""
        _, value = ops[0]
        column = self.field
        return cast(pw.ModelSelect, collection.where(column.contains(value)))
