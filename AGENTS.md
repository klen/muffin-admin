# AGENTS.md

Repository guide for coding agents working in `muffin-admin`.

## Stack and Layout

- Backend: Python package in `muffin_admin/`
- Frontend: React + TypeScript in `frontend/`
- Tests: `tests/` (Python), `frontend/src/*.test.*` (frontend)
- Python tooling config: `pyproject.toml`
- Python workflow shortcuts: root `Makefile`
- Documentation: MkDocs Material in `docs/`, config in `mkdocs.yml`
- Frontend workflow shortcuts: `frontend/Makefile`
- Git hooks: `.pre-commit-config.yaml`
- Commit convention: `.git-commits.yaml`

## Environment Setup

- Sync Python deps (CI-compatible): `uv sync --locked --all-extras --dev`
- Bootstrap local dev + install hooks: `make`
- Install frontend deps/build tooling: `make -C frontend`

## Build, Lint, Typecheck, Test Commands

### Python commands (run from repo root)

- Run full test suite: `make test` (Python + frontend)
- Run Python tests: `uv run pytest tests`
- Run one Python test file: `uv run pytest tests/test_basic.py`
- Run one Python test case: `uv run pytest tests/test_basic.py::test_endpoint`
- Run Python tests by expression: `uv run pytest tests -k "endpoint and not action"`
- Lint backend package: `uv run ruff check muffin_admin`
- Lint package + tests: `uv run ruff check muffin_admin tests`
- Format Python code: `uv run ruff format`
- Typecheck package: `uv run pyrefly check`
- Typecheck all (CI style): `uv run pyrefly check`

### Frontend commands (`frontend/`)

- Build TS output (`dist/`): `yarn build`
- Bundle with webpack: `make -C frontend`
- Start dev server: `make -C frontend dev`
- Watch webpack rebuilds: `make -C frontend watch`
- Typecheck frontend: `make -C frontend lint`
- Run frontend tests: `make -C frontend test` (or `cd frontend && yarn test`)

Single-test example: `cd frontend && npx vitest run src/dataprovider.test.ts`.
Use focused TS compile checks while editing:

- `cd frontend && npx tsc --noEmit --pretty src/index.tsx`

### Useful make targets (repo root)

- `make test` -> `uv run pytest tests` + `make -C frontend test`
- `make test-frontend` -> `make -C frontend test`
- `make lint` -> `pyrefly check` + `ruff check`
- `make front` -> build frontend
- `make example-peewee` -> run example app
- `make docs` -> `mkdocs build --strict`
- `make docs-serve` -> preview docs locally

## CI Baseline

Current CI (`.github/workflows/tests.yml`) runs:

- `uv sync --locked --all-extras --dev`
- `uv run pyrefly check`
- `uv run ruff check`
- `uv run pytest tests`
- `yarn install --frozen-lockfile` and `yarn test` in `frontend/`

`docs.yml` runs `uv run --locked --only-group docs mkdocs build --strict` and publishes to
GitHub Pages on `develop`.

Agent rule: before finishing non-trivial changes, run the checks relevant to touched code.

## Pre-commit and Commit Message Rules

Hooks run on `pre-commit`, `commit-msg`, and `pre-push`.

- `ruff format`
- `ruff check`
- `uv-lock --check`
- `pyrefly-check` (runs `uv run pyrefly check`)
- `uv run pytest tests` (pre-push)
- `make -C frontend test` (pre-push, when `frontend/` changes)
- plus standard sanity hooks (yaml/toml/merge/conflict/whitespace/debug)

Commit messages must follow conventional commits.
Allowed types from `.git-commits.yaml`:

- `chore`, `feat`, `fix`, `perf`, `refactor`, `style`, `test`, `build`, `ops`, `docs`, `merge`

## Code Style Guidelines

### Python formatting and structure

- Trust `ruff format` for canonical formatting.
- Max line length: `100`.
- Target syntax: Python `3.11+`.
- Prefer simple control flow and guard clauses over deep nesting.
- Keep functions single-purpose and easy to scan.

### Python imports

- Order imports as stdlib -> third-party -> local modules.
- Prefer absolute imports from `muffin_admin`.
- Put type-only imports inside `if TYPE_CHECKING:`.

### Python typing

- Add type hints for public APIs and non-trivial internals.
- Prefer modern annotations (`list[str]`, `dict[str, Any]`, `A | B`).
- Use `TypedDict`/type aliases for structured dictionaries.
- Keep `Any` constrained to integration boundaries.

### Python naming

- `snake_case`: functions, methods, variables, module names.
- `PascalCase`: classes.
- `UPPER_CASE`: constants.
- Tests: file `test_*.py`, function `test_*`.

### Python error handling

- Raise explicit API-level errors at HTTP boundaries (for example `APIError.BAD_REQUEST`).
- Preserve useful validation details in error responses when available.
- Use early returns for failed preconditions/auth checks.
- Avoid silent `except` blocks.

### Backend implementation patterns in this repo

- Resource handlers typically subclass `AdminHandler`.
- Behavior is commonly configured in nested `Meta` classes.
- Marshmallow schemas define input/output and validation.
- Most request handlers/actions are async; await I/O consistently.

### Frontend formatting and linting

- Biome config in `frontend/biome.json` is authoritative (format + lint + import sorting).
- Run `npx biome check --write` in `frontend/` to auto-fix formatting/lint issues.
- Semicolons are disabled.
- Print width is `100`.
- TS compile checks remain the primary enforced gate.

### Frontend typing and naming

- Prefer explicit exported types for public functions/components.
- `tsconfig` has `strict: false`; still write strict-friendly code when possible.
- `PascalCase` for React component files and components.
- `camelCase` for hooks/utilities (`useAction`, `buildRAComponent`, etc.).

### Frontend error handling

- Surface action/request errors through React Admin notifications.
- Throw explicit errors when required runtime state is missing.
- Prefer safe fallbacks (`null`, defaults) where behavior is optional.

## Documentation Guidance

- Pages live in `docs/` as Markdown and are built with MkDocs Material; `mkdocs.yml` has the
  `nav`. Add new pages to `nav` and link them from `docs/index.md`.
- `make docs` must pass `--strict` (CI fails on warnings such as a broken link or a page
  missing from `nav`).
- Keep `README.md` a short entry point; detailed material belongs in `docs/`.
- Code samples are taken from `muffin_admin/`, `example/` and `tests/`; do not invent options.

## Testing Guidance

- Add/adjust tests for behavior changes.
- Prefer focused tests for conversion and schema behavior.
- For handler/plugin changes, assert generated react-admin payloads.
- Reuse fixtures from `tests/conftest.py`.

## Cursor/Copilot Rules

No repository-specific rule files were found:

- `.cursorrules` - not present
- `.cursor/rules/` - not present
- `.github/copilot-instructions.md` - not present

If any of these files are added, treat them as high-priority instructions and update this guide.
