from example import app
from mixer.backend.peewee import Mixer
from example.models import Message, User


@app.manage.command
def devdata():
    mixer = Mixer(commit=True)
    statuses = [choice[0] for choice in Message.status.choices]
    mixer.cycle(20).blend(Message, status=mixer.RANDOM(*statuses))


@app.manage.command
def db():
    try:
        User.create_table()
        Message.create_table()
    except Exception:
        pass
