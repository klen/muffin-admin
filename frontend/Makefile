all: node_modules
	$(CURDIR)/node_modules/.bin/webpack

node_modules: package.json
	npm install
	touch node_modules

pypi:
	$(CURDIR)/node_modules/.bin/webpack

watch: node_modules
	$(CURDIR)/node_modules/.bin/webpack --watch

dev: node_modules
	NODE_ENV=development $(CURDIR)/node_modules/.bin/webpack serve

npm: node_modules
	$(CURDIR)/node_modules/.bin/babel src --out-dir dist/cjs

esm: node_modules
	$(CURDIR)/node_modules/.bin/babel src --no-babelrc --out-dir dist/esm --config-file ./babel.esm.json

clean:
	@rm -rf dist

build: clean npm esm
