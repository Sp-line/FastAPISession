from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy
from nats.js.api import DeliverPolicy

from core import fs_router, stream
from repositories.hall import HallRepository
from repositories.unit_of_work import UnitOfWork
from schemas.seat import SeatCreateEvent, SeatDeleteEvent


@fs_router.subscriber(
    "showtimes.seats.created",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
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
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
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
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def seats_deleted_hall_recalculate_capacity(
        payload: SeatDeleteEvent,
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.recalculate_and_update_capacity(payload.hall_id)
