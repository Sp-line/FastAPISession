from dishka.integrations.faststream import FromDishka

from core import fs_router, stream
from core.config import settings
from dependencies.faststream import NatsMsgIdDep
from event_handlers.base import base_consumer_config
from event_handlers.constants import HallDurables
from repositories import HallRepository
from schemas.seat import SeatCreateEvent, SeatDeleteEvent
from services import InboxUnitOfWork


@fs_router.subscriber(
    "showtimes.seats.created",
    stream=stream,
    pull_sub=True,
    durable=HallDurables.SESSION_SVC_SEATS_CREATED_HALL_RECALCULATE,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def seats_created_hall_recalculate_capacity(
        payload: SeatCreateEvent,
        repository: FromDishka[HallRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=HallDurables.SESSION_SVC_SEATS_CREATED_HALL_RECALCULATE,
    ) as should_proceed:
        if should_proceed:
            await repository.recalculate_and_update_capacity(payload.hall_id)


@fs_router.subscriber(
    "showtimes.seats.bulk.created",
    stream=stream,
    pull_sub=True,
    durable=HallDurables.SESSION_SVC_SEATS_BULK_CREATED_HALL_RECALCULATE,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def seats_bulk_created_hall_recalculate_capacity(
        payload: list[SeatCreateEvent],
        repository: FromDishka[HallRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=HallDurables.SESSION_SVC_SEATS_BULK_CREATED_HALL_RECALCULATE,
    ) as should_proceed:
        if should_proceed:
            await repository.recalculate_and_update_capacity(*{obj.hall_id for obj in payload})


@fs_router.subscriber(
    "showtimes.seats.deleted",
    stream=stream,
    pull_sub=True,
    durable=HallDurables.SESSION_SVC_SEATS_DELETED_HALL_RECALCULATE,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def seats_deleted_hall_recalculate_capacity(
        payload: SeatDeleteEvent,
        repository: FromDishka[HallRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=HallDurables.SESSION_SVC_SEATS_DELETED_HALL_RECALCULATE,
    ) as should_proceed:
        if should_proceed:
            await repository.recalculate_and_update_capacity(payload.hall_id)
