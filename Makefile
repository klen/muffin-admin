VIRTUAL_ENV ?= .venv
EXAMPLE = example

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

$(VIRTUAL_ENV): pyproject.toml
	@poetry install --with dev,example
	@poetry self add poetry-bumpversion
	@poetry run pre-commit install --hook-type pre-push
	@touch $(VIRTUAL_ENV)

.PHONY: test t
# target: test - Runs tests
test t: $(VIRTUAL_ENV)
	@poetry run pytest tests

db.sqlite: $(VIRTUAL_ENV)
	@poetry run muffin $(EXAMPLE) db
	@poetry run muffin $(EXAMPLE) devdata

.PHONY: locales
LOCALE ?= ru
locales: $(VIRTUAL_ENV)/bin/py.test db.sqlite
	@poetry run muffin $(EXAMPLE) extract_messages muffin_admin --locale $(LOCALE)
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
	make -j example-peewee front-dev

.PHONY: dev
mypy: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/mypy muffin_admin


.PHONY: example-peewee
# target: example-peewee - Run example
example-peewee: $(VIRTUAL_ENV) front
	@poetry run muffin example.peewee_orm db
	@poetry run muffin example.peewee_orm devdata
	@poetry run uvicorn example.peewee_orm:app --reload --port=8080


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
	@$(eval VFROM := $(shell poetry version -s))
	@poetry version $(VERSION)
	@git commit -am "Bump version $(VFROM) → `poetry version -s`"
	@git tag `poetry version -s`
	@git checkout master
	@git merge develop
	@git checkout develop
	@git push origin develop master
	@git push --tags

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release VERSION=patch

.PHONY: major
major:
	make release VERSION=major
