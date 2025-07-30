db.sqlite db:
	MUFFIN_AIOLIB=asyncio muffin peewee_orm db
	MUFFIN_AIOLIB=asyncio muffin peewee_orm devdata

BACKEND_PORT ?= 8080
peewee: db.sqlite
	MUFFIN_AIOLIB=asyncio uvicorn peewee_orm:app --reload --port=$(BACKEND_PORT) --http=httptools

sqlalchemy: db.sqlite
	MUFFIN_AIOLIB=asyncio uvicorn sqlalchemy_core:app --reload --port=8080 --http=httptools
