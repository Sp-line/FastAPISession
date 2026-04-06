from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy
from nats.js.api import DeliverPolicy
from pydantic import TypeAdapter

from core import fs_router, catalog_stream
from event_handlers.base import base_consumer_config
from event_handlers.constants import MovieDurables
from repositories import MovieRepository, UnitOfWork
from schemas.movie import MovieCreateEvent, MovieCreateDB, MovieUpdateEvent, MovieUpdateDB


@fs_router.subscriber(
    "catalog.movies.created",
    stream=catalog_stream,
    pull_sub=True,
    durable=MovieDurables.CATALOG_SVC_MOVIES_CREATED_SYNC_DB,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def movies_created_on_movie_microservice_sync_db(
        payload: MovieCreateEvent,
        repository: FromDishka[MovieRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.create(MovieCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "catalog.movies.bulk.created",
    stream=catalog_stream,
    pull_sub=True,
    durable=MovieDurables.CATALOG_SVC_MOVIES_BULK_CREATED_SYNC_DB,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def movies_bulk_created_on_movie_microservice_sync_db(
        payload: list[MovieCreateEvent],
        repository: FromDishka[MovieRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_create(
            TypeAdapter(list[MovieCreateDB]).validate_python(payload),
        )


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=catalog_stream,
    pull_sub=True,
    durable=MovieDurables.CATALOG_SVC_MOVIES_UPDATED_SYNC_DB,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def movies_updated_on_movie_microservice_sync_db(
        payload: MovieUpdateEvent,
        repository: FromDishka[MovieRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.update(payload.id, MovieUpdateDB(**payload.model_dump()))
