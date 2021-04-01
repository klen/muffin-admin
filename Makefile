VIRTUAL_ENV ?= env
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

# ==============
#  Bump version
# ==============

.PHONY: release
VERSION?=minor
# target: release - Bump version
release: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/bump2version $(VERSION)
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

# ===============
#  Build package
# ===============

.PHONY: upload
# target: upload - Upload module on PyPi
upload: clean $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/python setup.py bdist_wheel
	@$(VIRTUAL_ENV)/bin/twine check dist/*
	@$(VIRTUAL_ENV)/bin/twine upload dist/*.whl || true

# =============
#  Development
# =============

$(VIRTUAL_ENV): setup.cfg
	@[ -d $(VIRTUAL_ENV) ] || python -m venv $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install -e .[tests,build,example]
	@touch $(VIRTUAL_ENV)

.PHONY: test t
# target: test - Runs tests
test t: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pytest tests

db.sqlite: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/muffin $(EXAMPLE) db
	@$(VIRTUAL_ENV)/bin/muffin $(EXAMPLE) devdata

.PHONY: locales
LOCALE ?= ru
locales: $(VIRTUAL_ENV)/bin/py.test db.sqlite
	@$(VIRTUAL_ENV)/bin/muffin $(EXAMPLE) extract_messages muffin_admin --locale $(LOCALE)
	@$(VIRTUAL_ENV)/bin/muffin $(EXAMPLE) compile_messages

.PHONY: frontend
frontend:
	make -C frontend

.PHONY: frontend-watch
frontend-watch:
	make -C frontend watch

.PHONY: frontend-dev
frontend-dev:
	make -C frontend dev

.PHONY: dev
dev:
	make -j example-peewee frontend-dev

.PHONY: dev
mypy: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/mypy muffin_admin


.PHONY: example-peewee
# target: example-peewee - Run example
example-peewee: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/muffin examples.peewee_orm db
	@$(VIRTUAL_ENV)/bin/muffin examples.peewee_orm devdata
	@$(VIRTUAL_ENV)/bin/uvicorn examples.peewee_orm:app --reload --port=5000

.PHONY: example-sqlalchemy
# target: example-sqlalchemy - Run example
example-sqlalchemy: $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/uvicorn examples.sqlalchemy_core:app --reload --port=5000
