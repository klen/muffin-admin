"""SQLAlchemy core support."""

import typing as t

import marshmallow as ma
from muffin_rest.sqlalchemy import SARESTOptions, SARESTHandler, SAFilter, Filter
from sqlalchemy import Enum

from ..handler import AdminHandler, AdminOptions


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
            self.filters = [SAFilter('id', column=self.table_pk), *self.filters]


class SAAdminHandler(AdminHandler, SARESTHandler):

    """Work with SQLAlchemy Core."""

    meta_class: t.Type[SAAdminOptions] = SAAdminOptions

    class Meta:

        """Mark the class as abc base."""

        abc = True

    @classmethod
    def to_ra_input(cls, field: ma.fields.Field, name: str) -> t.Optional[t.Tuple[str, t.Dict]]:
        """Convert self schema field to ra field."""
        res = super(SAAdminHandler, cls).to_ra_input(field, name)
        if res:
            column = getattr(cls.meta.table.c, field.attribute or name, None)
            if isinstance(column.type, Enum):
                rtype, props = res
                return 'SelectInput', dict(props, choices=[
                    {"id": c.value, "name": c.name} for c in column.type.enum_class
                ])

        return res
