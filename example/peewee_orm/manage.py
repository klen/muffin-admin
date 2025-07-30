"""Custom CLI commands for the application."""

from random import choice

from mixer.backend.peewee import Mixer

from . import app
from .database import Message, User
from .database import db as database


@app.manage.shell
def shell():
    """Open an interactive shell with the application context."""
    ctx = {"app": app}
    ctx.update(app.plugins)
    for Model in database.manager.models:
        ctx[Model.__name__] = Model

    return ctx


@app.manage
async def db():
    """Simple DB schema creation. For real case use a migration engine."""
    async with database:
        await database.create_tables()


@app.manage
async def devdata():
    """Generate some fake data."""
    mixer = Mixer(commit=True)

    async with database.connection():
        await User.get_or_create(
            email="admin@admin.com",
            defaults={
                "password": "admin",
                "role": "admin",
                "first_name": "Admin",
                "last_name": "General",
                "picture": "https://picsum.photos/id/10/100",
            },
        )

        await User.get_or_create(
            email="manager@admin.com",
            defaults={
                "password": "manager",
                "role": "manager",
                "first_name": "Manager",
                "last_name": "Throw",
                "picture": "https://picsum.photos/id/20/100",
            },
        )

        # Generate 100 users
        num_users = await User.select().count()
        for n in range(100 - num_users):
            await User.create(
                email=mixer.faker.email(),
                role="user",
                picture=f"https://picsum.photos/id/2{n}/100",
                first_name=mixer.faker.first_name(),
                last_name=mixer.faker.last_name(),
            )

        # Generate 100 messages
        statuses = [choice[0] for choice in Message.status.choices]
        users = await User.select()
        for n in range(100):
            await Message.create(
                body=mixer.faker.text(),
                title=mixer.faker.title(),
                user=choice(users),  # noqa: S311
                status=mixer.faker.random.choice(statuses),
            )
