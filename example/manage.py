from example import app
from mixer.backend.peewee import Mixer
from example.models import Test


@app.manage.command
def devdata():
    mixer = Mixer(commit=True)
    statuses = [choice[0] for choice in Test.status.choices]
    mixer.cycle(20).blend(Test, status=mixer.RANDOM(*statuses))


@app.manage.command
def db():
    try:
        Test.create_table()
    except Exception:
        pass
