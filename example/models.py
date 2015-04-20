import peewee as pw

from example import app


@app.ps.peewee.register
class Test(app.ps.peewee.TModel):

    active = pw.BooleanField()
    content = pw.CharField()
