# Development

The project uses `uv` for dependencies, `ruff` for formatting and linting, `pyrefly` for types,
`pytest` for tests, and yarn/webpack for the frontend bundle.

## Setup

```bash
make
```

`make` runs `uv sync` and installs the pre-commit hooks. The equivalent manual steps:

```bash
uv sync --locked --all-extras --dev
uv run pre-commit install
```

Python 3.11 or newer is required. CI runs 3.11 through 3.15.

## Checks

Run the same order as CI:

```bash
uv run pyrefly check
uv run ruff check
uv run pytest tests
```

`make lint` runs `pyrefly check` and `ruff check`. `make test` runs the Python and
frontend test suites; `make test-frontend` runs only `frontend/` tests.

Pytest defaults come from `pyproject.toml` (`-xsv`), so the suite stops on the first failure.
A focused run:

```bash
uv run pytest tests/test_peewee.py
uv run pytest tests/test_plugin.py::test_auth
uv run pytest tests -k "cookies"
```

The suite uses SQLite only; no Postgres or Mongo services are needed. Base and plugin tests run
under asyncio, trio and curio through the `aiolib` fixture; backend tests pin asyncio.

An autouse fixture writes a stub `muffin_admin/main.js` for the duration of the session and
restores any existing file afterwards, so tests do not need a built frontend and do not destroy
the local bundle.

## Pre-commit

Hooks run on `pre-commit`, `commit-msg` and `pre-push`:

- `ruff format` and `ruff check`
- `pyrefly check`
- `uv lock --check`
- `uv run pytest tests` on pre-push
- `make -C frontend test` on pre-push when `frontend/` changes
- the usual YAML/TOML, whitespace and merge-conflict checks

If dependency metadata changes, run `uv lock` before committing. Commit messages must follow
the conventional types in `.git-commits.yaml`: `build`, `chore`, `docs`, `feat`, `fix`, `merge`,
`ops`, `perf`, `refactor`, `style`, `test`.

## Docs

```bash
make docs          # mkdocs build --strict into site/
make docs-serve    # preview at http://127.0.0.1:8000
```

The `docs` dependency group is separate from `dev`, so database drivers and test tools are not
installed just to build the site. When adding a page, add it to `nav` in `mkdocs.yml` and link
it from `docs/index.md`.

`.github/workflows/docs.yml` builds the site on pull requests and publishes it to GitHub Pages
on pushes to `develop`. The repository must have Pages enabled with the source set to GitHub
Actions.

## Examples

The examples run against SQLite:

```bash
make example-peewee     # build the frontend, create example/db.sqlite, serve :8080
make example-sqlalchemy
```

They create a hundred users, messages and orders, with `admin@admin.com:admin` available for
login. The frontend dev server proxies to the backend on :5555:

```bash
make dev                # backend on :5555 plus the webpack dev server
```

The example applications are `example/peewee_orm/` and `example/sqlalchemy_core/`; both share
`example/views.py` and `example/admin.css`.

## Frontend

```bash
make -C frontend        # yarn install if needed, then webpack -> muffin_admin/main.js
make -C frontend lint   # tsc --noEmit
make -C frontend test   # vitest (data provider, file URLs, dashboard)
make -C frontend dev    # webpack dev server
make -C frontend watch  # rebuild on change
```

Webpack writes the bundle to `muffin_admin/main.js` (and the license notice to
`muffin_admin/main.js.LICENSE.txt`). Both are gitignored. `yarn build` in `frontend/` only
compiles the TypeScript library into `frontend/dist/`.

## Layout

- `muffin_admin/plugin.py`: the Muffin plugin, routes, `ra.json` serialization
- `muffin_admin/handler.py`: `AdminOptions`, `AdminHandler`, action decorator, marshmallow to
  react-admin mapping
- `muffin_admin/peewee/`, `muffin_admin/sqlalchemy/`: backend handlers and options
- `muffin_admin/types.py`: `TypedDict` and type aliases used by the handler API
- `muffin_admin/admin.html`: the page template, read at import time
- `frontend/`: react-admin application, built into `muffin_admin/main.js`

## Release

Releases are cut from `develop` into `main`:

```bash
make release          # minor by default
make patch
make major
```

`make release` bumps the version with `bump-my-version`, updates `uv.lock`, creates a release
commit and tag, pushes `main`, and merges back into `develop`. `bumpversion` keeps three files
in sync:

- `pyproject.toml`
- `frontend/package.json`
- `frontend/src/version.ts`

`.github/workflows/release.yml` runs after tests pass on `main`. It builds and publishes the
frontend npm package, then runs `make pypi` in `frontend/` so `muffin_admin/main.js` exists,
and only then runs `uv build` and `uv publish`. The Python package is built from the source
tree, and `uv_build` includes everything under `muffin_admin/`, so the bundle and its license
notice end up in both the wheel and the sdist.

A `uv build` outside the release workflow (a clean checkout without a frontend build) still
succeeds, but the resulting package has no `main.js` and the admin page will not work.
