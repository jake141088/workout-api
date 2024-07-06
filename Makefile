##Ele abrevia alguns comando que devem ser muito executados
.PHONY: run

run:
    uvicorn main:app --reload

create-migrations:
    @PYHTONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(d)

run_migrations:
    @PYTHONPATH=$PYHTONPATH:$(pwd) alembic upgrade head