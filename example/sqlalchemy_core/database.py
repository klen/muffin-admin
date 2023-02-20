import datetime as dt
import enum
from pathlib import Path

import sqlalchemy as sa
from muffin_databases import Plugin

from . import app


# We will use Peewee as ORM, so connect the related plugin
db = Plugin(app, url=f"sqlite:///{ Path(__file__).parent.parent / 'db.sqlite' }")

meta = sa.MetaData()


class Roles(enum.Enum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


User = sa.Table(
    'user', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('created', sa.DateTime, default=dt.datetime.utcnow, nullable=False),
    sa.Column('email', sa.String(255), nullable=False),
    sa.Column('first_name', sa.String(255)),
    sa.Column('last_name', sa.String(255)),
    sa.Column('password', sa.String(255)),
    sa.Column('picture', sa.String(255), default="https://picsum.photos/200"),
    sa.Column('is_active', sa.Boolean, default=True),
    sa.Column('meta', sa.JSON, default={}),
    sa.Column('role', sa.Enum(Roles), default=Roles.user, nullable=False),
)


class Statuses(enum.Enum):
    new = 'new'
    published = 'published'


Message = sa.Table(
    'message', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('created', sa.DateTime, default=dt.datetime.utcnow, nullable=False),
    sa.Column('status', sa.Enum(Statuses), default=Statuses.new, nullable=False),
    sa.Column('title', sa.String(255), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('user_id', sa.ForeignKey('user.id'), nullable=False),
)
