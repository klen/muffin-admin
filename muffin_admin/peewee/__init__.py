"""Peewee ORM Support."""

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Type, cast

import peewee as pw
from muffin_peewee import JSONLikeField
from muffin_rest.peewee import PWRESTBase
from muffin_rest.peewee.filters import PWFilter
from muffin_rest.peewee.options import PWRESTOptions

from muffin_admin.handler import AdminHandler, AdminOptions

if TYPE_CHECKING:
    import marshmallow as ma

    from muffin_admin.typing import RA_INFO


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

    meta_class: Type[PWAdminOptions] = PWAdminOptions
    meta: PWAdminOptions

    @classmethod
    def to_ra_field(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA fields."""
        model_field = getattr(cls.meta.model, field.attribute or source, None)
        if model_field and (
            isinstance(model_field, JSONLikeField) or model_field.field_type.lower() == "json"
        ):
            return "JsonField", {}

        return super(PWAdminHandler, cls).to_ra_field(field, source)

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, source: str) -> RA_INFO:
        """Setup RA inputs."""
        model_field = getattr(cls.meta.model, field.attribute or source, None)
        ra_type, props = super(PWAdminHandler, cls).to_ra_input(field, source)
        if model_field:
            if model_field.choices:
                return "SelectInput", dict(
                    props,
                    choices=[{"id": c[0], "name": c[1]} for c in model_field.choices],
                )

            if isinstance(model_field, pw.TextField):
                return "TextInput", dict(props, multiline=True)

            if isinstance(model_field, JSONLikeField) or model_field.field_type.lower() == "json":
                return "JsonInput", props

            if isinstance(model_field, pw.ForeignKeyField) and source in cls.meta.references:
                ref, _, ref_source = cls.meta.references[source].partition(".")
                return "FKInput", dict(
                    props,
                    refProp=ref_source or ref,
                    refSource=model_field.rel_field.name,
                    reference=ref_source and ref or model_field.rel_model._meta.table_name,
                )

        return ra_type, props


class PWSearchFilter(PWFilter):

    """Search in query by value."""

    def query(self, qs: pw.Query, column: pw.Field, *ops: Tuple, **_) -> pw.Query:
        """Apply the filters to Peewee QuerySet.."""
        _, value = ops[0]
        return cast(pw.Query, qs.where(column.contains(value)))
