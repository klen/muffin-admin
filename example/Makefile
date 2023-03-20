db.sqlite:
	muffin peewee_orm db
	muffin peewee_orm devdata

BACKEND_PORT ?= 8080
peewee: db.sqlite
	uvicorn peewee_orm:app --reload --port=$(BACKEND_PORT)

sqlalchemy: db.sqlite
	uvicorn sqlalchemy_core:app --reload --port=8080
