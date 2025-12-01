import marshmallow as ma
from marshmallow_peewee import ModelSchema

from example.peewee_orm.database import User


class GreetActionSchema(ma.Schema):
    name = ma.fields.String(required=True)


class UserSchema(ModelSchema):
    name = ma.fields.Function(lambda u: f"{u.first_name} {u.last_name}")
    picture = ma.fields.Raw()

    class Meta:
        model = User
        dump_only = ("created",)
        load_only = ("password",)
