db.sqlite:
	muffin peewee_orm db
	muffin peewee_orm devdata

peewee: db.sqlite
	uvicorn peewee_orm:app --reload --port=5000

sqlalchemy: db.sqlite
	uvicorn sqlalchemy_core:app --reload --port=5000
