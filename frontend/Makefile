all: node_modules
	$(CURDIR)/node_modules/.bin/webpack

node_modules: package.json
	yarn
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

lint:
	# npx lint
	npx tsc --noEmit --pretty


build: clean npm esm
