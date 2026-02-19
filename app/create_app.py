from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.models import db_helper
from dependencies import InfrastructureProvider, RepositoryProvider, ServiceProvider


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

    return app
