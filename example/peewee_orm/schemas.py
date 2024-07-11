import marshmallow as ma


class GreetActionSchema(ma.Schema):
    name = ma.fields.String(required=True)
