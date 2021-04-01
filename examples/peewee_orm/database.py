"""Setup application's models."""

import datetime as dt
from pathlib import Path

import peewee as pw
from muffin_peewee import Plugin

from . import app


db = Plugin(app, connection=f"sqlite:///{ Path(__file__).parent.parent / 'db.sqlite' }")


class BaseModel(pw.Model):

    """Automatically keep the model's creation time."""

    created = pw.DateTimeField(default=dt.datetime.utcnow)


@db.register
class User(BaseModel):

    """A simple user model."""

    email = pw.CharField()
    password = pw.CharField(null=True)  # not secure only for the example

    is_active = pw.BooleanField(default=True)
    role = pw.CharField(choices=(('user', 'user'), ('manager', 'manager'), ('admin', 'admin')))


@db.register
class Message(BaseModel):

    """Just a users' messages."""

    status = pw.CharField(choices=(('new', 'new'), ('published', 'published')))
    title = pw.CharField()
    body = pw.TextField()

    user = pw.ForeignKeyField(User)
