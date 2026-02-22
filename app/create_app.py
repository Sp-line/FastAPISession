from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka
from dishka.integrations.faststream import setup_dishka as setup_faststream_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import event_handlers  # noqa: F401
from core import fs_router
from core.models import db_helper
from dependencies import InfrastructureProvider, RepositoryProvider, ServiceProvider
from exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def create() -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    container = make_async_container(
        InfrastructureProvider(),
        RepositoryProvider(),
        ServiceProvider(),
    )

    setup_fastapi_dishka(container, app)
    setup_faststream_dishka(container, broker=fs_router.broker, auto_inject=True)

    app.include_router(fs_router)
    register_exception_handlers(app)

    return app
