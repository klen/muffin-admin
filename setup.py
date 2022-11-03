"""Setup the package."""


import pathlib

# Parse requirements
# ------------------
import pkg_resources


def parse_requirements(path: str) -> "list[str]":
    with pathlib.Path(path).open() as requirements:
        return [str(req) for req in pkg_resources.parse_requirements(requirements)]


# Setup package
# -------------

from setuptools import setup

setup(
    install_requires=parse_requirements("requirements/requirements.txt"),
    extras_require={
        "tests": parse_requirements("requirements/requirements-tests.txt"),
        "yaml": ["pyyaml"],
        "build": ["bump2version", "wheel"],
        "peewee": ["muffin-peewee-aio", "marshmallow-peewee >= 3.4.1"],
        "sqlalchemy": [
            "muffin-databases    >= 0.3.2",
            "marshmallow-sqlalchemy",
            "sqlalchemy",
        ],
    },
)

# pylama:ignore=E402,D
