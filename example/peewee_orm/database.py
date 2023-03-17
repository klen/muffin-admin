"""Setup application's models."""

import datetime as dt
from pathlib import Path

import peewee as pw
from muffin_peewee import JSONLikeField, Plugin
from peewee_aio.model import AIOModel

from . import app

db = Plugin(app, connection=f"sqlite:///{ Path(__file__).parent.parent / 'db.sqlite' }")


class BaseModel(AIOModel):

    """Automatically keep the model's creation time."""

    created = pw.DateTimeField(default=dt.datetime.utcnow)


@db.register
class Group(BaseModel):

    """A group."""

    name = pw.CharField(max_length=255, unique=True)


@db.register
class User(BaseModel):

    """A simple user model."""

    email = pw.CharField()
    first_name = pw.CharField(null=True, help_text="First name")
    last_name = pw.CharField(null=True)
    password = pw.CharField(null=True)  # not secure only for the example
    picture = pw.CharField(
        default="https://picsum.photos/100",
        help_text="Full URL to the picture",
    )
    meta = JSONLikeField(default={})

    is_active = pw.BooleanField(default=True)
    role = pw.CharField(
        choices=(("user", "user"), ("manager", "manager"), ("admin", "admin")),
    )

    # Relationships
    group = pw.ForeignKeyField(Group, backref="users", null=True)


@db.register
class Message(BaseModel):

    """Just a users' messages."""

    status = pw.CharField(choices=(("new", "new"), ("published", "published")))
    title = pw.CharField()
    body = pw.TextField()
    dtpublish = pw.DateTimeField(null=True)

    user = pw.ForeignKeyField(User)
