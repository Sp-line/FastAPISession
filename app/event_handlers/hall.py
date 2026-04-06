from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy
from nats.js.api import DeliverPolicy

from core import fs_router, stream
from event_handlers.base import base_consumer_config
from event_handlers.constants import HallDurables
from repositories import HallRepository, UnitOfWork
from schemas.seat import SeatCreateEvent, SeatDeleteEvent


@fs_router.subscriber(
    "showtimes.seats.created",
    stream=stream,
    pull_sub=True,
    durable=HallDurables.SHOWTIMES_SVC_SEATS_CREATED_HALL_RECALCULATE,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def seats_created_hall_recalculate_capacity(
        payload: SeatCreateEvent,
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.recalculate_and_update_capacity(payload.hall_id)


@fs_router.subscriber(
    "showtimes.seats.bulk.created",
    stream=stream,
    pull_sub=True,
    durable=HallDurables.SHOWTIMES_SVC_SEATS_BULK_CREATED_HALL_RECALCULATE,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def seats_bulk_created_hall_recalculate_capacity(
        payload: list[SeatCreateEvent],
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.recalculate_and_update_capacity(*{obj.hall_id for obj in payload})


@fs_router.subscriber(
    "showtimes.seats.deleted",
    stream=stream,
    pull_sub=True,
    durable=HallDurables.SHOWTIMES_SVC_SEATS_DELETED_HALL_RECALCULATE,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def seats_deleted_hall_recalculate_capacity(
        payload: SeatDeleteEvent,
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.recalculate_and_update_capacity(payload.hall_id)
