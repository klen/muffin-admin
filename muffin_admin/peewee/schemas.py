from marshmallow_peewee import ModelSchema


class PeeweeModelSchema(ModelSchema):
    class Meta:
        datetimeformat = "timestamp_ms"
