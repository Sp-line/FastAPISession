from fastapi import FastAPI

from exceptions.db_handlers import register_db_exception_handlers


def register_exception_handlers(app: FastAPI) -> None:
    register_db_exception_handlers(app)
