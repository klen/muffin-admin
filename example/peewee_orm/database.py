"""Setup application's models."""

import datetime as dt
from pathlib import Path

import peewee as pw
from muffin_peewee import JSONLikeField, Plugin
from peewee_aio import AIOModel, fields

from . import app

db = Plugin(app, connection=f"sqlite:///{Path(__file__).parent.parent / 'db.sqlite'}")


class BaseModel(AIOModel):
    """Automatically keep the model's creation time."""

    created = fields.DateTimeField(default=dt.datetime.utcnow)


@db.register
class Group(BaseModel):
    """A group."""

    name = fields.CharField(max_length=255, unique=True)


@db.register
class User(BaseModel):
    """A simple user model."""

    email = fields.CharField(primary_key=True)
    first_name = fields.CharField(null=True, help_text="First name")
    last_name = fields.CharField(null=True)
    password = fields.CharField(null=True)  # not secure only for the example
    picture = fields.CharField(
        default="https://picsum.photos/100",
        help_text="Full URL to the picture",
    )
    meta = JSONLikeField(default={})

    is_active = fields.BooleanField(default=True)
    role = fields.CharField(
        choices=(("user", "user"), ("manager", "manager"), ("admin", "admin")),
    )

    # Relationships
    group = fields.ForeignKeyField(Group, backref="users", null=True)


@db.register
class Message(BaseModel):
    """Just a users' messages."""

    status = fields.CharField(choices=(("new", "new"), ("published", "published")))
    title = fields.CharField()
    body = fields.TextField()
    dtpublish = fields.DateTimeField(null=True)

    user = fields.ForeignKeyField(User, help_text="Choose a user")


@db.register
class Order(BaseModel):
    source = fields.CharField()
    source_id = fields.CharField()

    amount = fields.IntegerField()
    currency = fields.CharField()

    class Meta:
        primary_key = pw.CompositeKey("source", "source_id")
