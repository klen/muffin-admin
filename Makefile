VIRTUAL_ENV ?= .venv
EXAMPLE = example
PACKAGE = muffin_admin

all: $(VIRTUAL_ENV)

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Display callable targets
clean:
	rm -rf build/ dist/ docs/_build *.egg-info
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR)/$(MODULE) -name "__pycache__" | xargs rm -rf

# =============
#  Development
# =============

$(VIRTUAL_ENV): pyproject.toml .pre-commit-config.yaml
	@poetry install --with dev,example
	@poetry self add poetry-bumpversion
	@poetry run pre-commit install
	@touch $(VIRTUAL_ENV)

.PHONY: test t
# target: test - Runs tests
test t: $(VIRTUAL_ENV)
	@poetry run pytest tests

example/db.sqlite: $(VIRTUAL_ENV)
	@poetry run muffin $(EXAMPLE) db
	@poetry run muffin $(EXAMPLE) devdata

sqlite: example/db.sqlite
	sqlite3 example/db.sqlite

.PHONY: locales
LOCALE ?= ru
locales: $(VIRTUAL_ENV)/bin/py.test db.sqlite
	@poetry run muffin $(EXAMPLE) extract_messages $(PACKAGE) --locale $(LOCALE)
	@poetry run muffin $(EXAMPLE) compile_messages

.PHONY: front
front:
	make -C frontend

.PHONY: front-watch
front-watch:
	make -C frontend watch

.PHONY: front-dev
front-dev:
	make -C frontend dev

.PHONY: dev
dev:
	BACKEND_PORT=5555 make -j example-peewee front-dev

.PHONY: lint
lint: $(VIRTUAL_ENV)
	@poetry run mypy $(PACKAGE)
	@poetry run ruff check $(PACKAGE)


BACKEND_PORT ?= 8080
.PHONY: example-peewee
# target: example-peewee - Run example
example-peewee: $(VIRTUAL_ENV) front
	@poetry run muffin example.peewee_orm db
	@poetry run muffin example.peewee_orm devdata
	@poetry run uvicorn example.peewee_orm:app --reload --port=$(BACKEND_PORT)


shell: $(VIRTUAL_ENV)
	@poetry run muffin example.peewee_orm shell

.PHONY: example-sqlalchemy
# target: example-sqlalchemy - Run example
example-sqlalchemy: $(VIRTUAL_ENV) front
	@poetry run uvicorn example.sqlalchemy_core:app --reload --port=8080

# ==============
#  Bump version
# ==============

.PHONY: release
VERSION?=minor
# target: release - Bump version
release: $(VIRTUAL_ENV)
	git checkout develop
	git pull
	git checkout master
	git merge develop
	git pull
	@poetry version $(VERSION)
	git commit -am "build(release): `poetry version -s`"
	git tag `poetry version -s`
	git checkout develop
	git merge master
	git push --tags origin develop master

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release VERSION=patch

.PHONY: major
major:
	make release VERSION=major

v:
	@echo `poetry version -s`
