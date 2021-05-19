all: node_modules
	$(CURDIR)/node_modules/.bin/webpack

node_modules: package.json
	npm install

watch: node_modules
	$(CURDIR)/node_modules/.bin/webpack --watch

dev: node_modules
	NODE_ENV=development $(CURDIR)/node_modules/.bin/webpack serve
