VIRTUAL_ENV ?= $(shell echo "$${VIRTUAL_ENV:-.env}")

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
release:
	@$(VIRTUAL_ENV)/bin/pip install bumpversion
	@$(VIRTUAL_ENV)/bin/bumpversion $(VERSION)
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

.PHONY: register
# target: register - Register module on PyPi
register:
	@$(VIRTUAL_ENV)/bin/python setup.py register

.PHONY: upload
# target: upload - Upload module on PyPi
upload: clean
	@$(VIRTUAL_ENV)/bin/pip install twine wheel
	@$(VIRTUAL_ENV)/bin/python setup.py sdist bdist_wheel
	@$(VIRTUAL_ENV)/bin/twine upload dist/*

# =============
#  Development
# =============

$(VIRTUAL_ENV): requirements.txt
	@[ -d $(VIRTUAL_ENV) ] || virtualenv --no-site-packages --python=python3 $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install -r requirements.txt
	@touch $(VIRTUAL_ENV)

$(VIRTUAL_ENV)/bin/py.test: $(VIRTUAL_ENV) requirements-tests.txt
	@$(VIRTUAL_ENV)/bin/pip install -r requirements-tests.txt
	@touch $(VIRTUAL_ENV)/bin/py.test

.PHONY: test
# target: test - Runs tests
test: $(VIRTUAL_ENV)/bin/py.test
	@$(VIRTUAL_ENV)/bin/py.test -xs tests.py

.PHONY: t
t: test

.PHONY: run
run: $(VIRTUAL_ENV)/bin/py.test db.sqlite
	@$(VIRTUAL_ENV)/bin/muffin example run --bind=0.0.0.0:5000 --timeout=3000

db.sqlite: $(VIRTUAL_ENV)/bin/py.test
	@$(VIRTUAL_ENV)/bin/muffin example db
	@$(VIRTUAL_ENV)/bin/muffin example devdata

.PHONY: daemon
daemon: $(VIRTUAL_ENV)/bin/py.test daemon-kill
	@while nc localhost 5000; do echo 'Waiting for port' && sleep 2; done
	@$(VIRTUAL_ENV)/bin/muffin example run --bind=0.0.0.0:5000 --pid=$(CURDIR)/pid --daemon

.PHONY: daemon-kill
daemon-kill:
	@[ -r $(CURDIR)/pid ] && echo "Kill daemon" `cat $(CURDIR)/pid` && kill `cat $(CURDIR)/pid` || true

.PHONY: watch
watch:
	@make daemon
	@(fswatch -0or $(CURDIR)/example -e "__pycache__" | xargs -0n1 -I {} make daemon) || make daemon-kill
