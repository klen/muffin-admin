import peewee as pw

from example import app


@app.ps.peewee.register
class User(app.ps.peewee.TModel):

    name = pw.CharField()

    def __str__(self):
        return self.name

    __unicode__ = __str__


@app.ps.peewee.register
class Message(app.ps.peewee.TModel):

    active = pw.BooleanField()
    status = pw.CharField(choices=list(zip(('new', 'done'), ('new', 'done'))))
    content = pw.CharField()

    user = pw.ForeignKeyField(User)
