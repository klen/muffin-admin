import peewee as pw

from example import app


@app.ps.peewee.register
class Test(app.ps.peewee.TModel):

    active = pw.BooleanField()
    status = pw.CharField(choices=list(zip(('new', 'done'), ('new', 'done'))))
    content = pw.CharField()
