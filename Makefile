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
	@uv sync
	@uv run pre-commit install
	@touch $(VIRTUAL_ENV)

.PHONY: test t
# target: test - Runs tests
test t: $(VIRTUAL_ENV)
	@uv run pytest tests

example/db.sqlite: $(VIRTUAL_ENV)
	@uv run muffin $(EXAMPLE) db
	@uv run muffin $(EXAMPLE) devdata

sqlite: example/db.sqlite
	sqlite3 example/db.sqlite

.PHONY: locales
LOCALE ?= ru
locales: $(VIRTUAL_ENV)/bin/py.test db.sqlite
	@uv run muffin $(EXAMPLE) extract_messages $(PACKAGE) --locale $(LOCALE)
	@uv run muffin $(EXAMPLE) compile_messages

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
	@uv run mypy $(PACKAGE)
	@uv run ruff check $(PACKAGE)


BACKEND_PORT ?= 8080
.PHONY: example-peewee
# target: example-peewee - Run example
example-peewee: $(VIRTUAL_ENV) front
	@MUFFIN_AIOLIB=asyncio uv run muffin example.peewee_orm db
	@MUFFIN_AIOLIB=asyncio uv run muffin example.peewee_orm devdata
	@MUFFIN_AIOLIB=asyncio uv run uvicorn example.peewee_orm:app --reload --port=$(BACKEND_PORT)


shell: $(VIRTUAL_ENV)
	@uv run muffin example.peewee_orm shell

.PHONY: example-sqlalchemy
# target: example-sqlalchemy - Run example
example-sqlalchemy: $(VIRTUAL_ENV) front
	@uv run uvicorn example.sqlalchemy_core:app --reload --port=8080

# ==============
#  Bump version
# ==============

VERSION	?= minor
MAIN_BRANCH = master

.PHONY: release
VPART?=minor
# target: release - Bump version
release:
	git checkout master
	git pull
	git checkout develop
	git pull
	uvx bump-my-version bump $(VPART)
	uv lock
	@VERSION="$$(uv version --short)"; \
		{ \
			printf 'build(release): %s\n\n' "$$VERSION"; \
			printf 'Changes:\n\n'; \
			git log --oneline --pretty=format:'%s [%an]' $(MAIN_BRANCH)..develop | grep -Evi 'github|^Merge' || true; \
		} | git commit -a -F -; \
		git tag "$$VERSION";
	git checkout $(MAIN_BRANCH)
	git merge develop
	git checkout develop
	git merge $(MAIN_BRANCH)
	git push origin develop $(MAIN_BRANCH) --tags
	@echo "Release process complete for `uv version --short`"

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release VPART=patch

.PHONY: major
major:
	make release VPART=major

version v:
	uv version --short
