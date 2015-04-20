from example import app
from mixer.backend.peewee import Mixer
from example.models import Test


@app.manage.command
def devdata():
    mixer = Mixer(commit=True)
    mixer.cycle(20).blend(Test)


@app.manage.command
def db():
    Test.create_table()
