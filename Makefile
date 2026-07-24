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

RELEASE	?= minor
MANAGER	?= uv

.PHONY: release
# target: release - Bump version
release:
	@echo "Starting release process (bumping $(RELEASE) version)..."
	@git checkout main
	@git pull
	@git checkout develop
	@git pull
	@echo "Bumping version and creating release commit and tag..."
	@uvx bump-my-version bump $(RELEASE)
	@echo "Version bumped to `$(MANAGER) version --short`."
	@$(MANAGER) lock
	@echo "Committing version bump and creating tag..."
	@VERSION=`$(MANAGER) version --short`; \
		{ \
			printf 'build(release): %s\n\n' "$$VERSION"; \
			printf 'Changes:\n\n'; \
			git log --oneline --pretty=format:'%s [%an]' main..develop | grep -Evi 'github|^Merge' || true; \
		} | git commit -a -F -
	@echo "Merging changes between branches..."
	@git checkout main
	@git merge --ff-only develop
	@VERSION=`$(MANAGER) version --short`; \
		git push origin main; \
		git tag -a "$$VERSION" -m "$$VERSION"; \
		git push origin "$$VERSION"
	@git checkout develop
	@git merge --ff-only main
	@git push origin develop
	@echo "Release process complete for `$(MANAGER) version --short`"

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release RELEASE=patch

.PHONY: major
major:
	make release RELEASE=major

version v:
	uv version --short
