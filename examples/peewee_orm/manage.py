"""Custom CLI commands for the application."""

from mixer.backend.peewee import Mixer

from . import app
from .database import User, Message


@app.manage
def db():
    """Simple DB schema creation. For real case use a migration engine."""
    try:
        User.create_table()
        Message.create_table()
    except Exception:
        pass


@app.manage
def devdata():
    """Generate some fake data."""
    mixer = Mixer(commit=True)

    # Generate admin user if not exists
    mixer.guard(User.email == 'admin@admin.com').blend(
        User, email='admin@admin.com', password='admin', role='admin')

    # Generate manager user if not exists
    mixer.guard(User.email == 'manager@admin.com').blend(
        User, email='admin@manager.com', password='manager', role='manager')

    # Generate 100 users
    if User.select().count() < 100:
        mixer.cycle(100).blend(User, role='user')

    # Generate 100 messages
    statuses = [choice[0] for choice in Message.status.choices]
    mixer.cycle(100).blend(Message, user=mixer.SELECT, status=mixer.RANDOM(*statuses))
