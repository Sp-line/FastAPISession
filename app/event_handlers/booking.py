from dishka.integrations.faststream import FromDishka

from core import fs_router, purchases_stream
from core.config import settings
from dependencies.faststream import NatsMsgIdDep
from event_handlers.base import base_consumer_config
from event_handlers.constants import BookingDurables
from repositories import BookingRepository
from schemas.booking import BookingCreateDB, BookingDeleteDB
from schemas.ticket import TicketCreateEvent, TicketUpdateEvent, TicketDeleteEvent
from services import InboxUnitOfWork
from services.ticket import TicketStatusAdapter


@fs_router.subscriber(
    "purchases.tickets.created",
    stream=purchases_stream,
    pull_sub=True,
    durable=BookingDurables.SESSION_SVC_TICKETS_CREATED_BOOKING_CREATE,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def ticket_created_on_order_microservice_booking_create(
        payload: TicketCreateEvent,
        repository: FromDishka[BookingRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=BookingDurables.SESSION_SVC_TICKETS_CREATED_BOOKING_CREATE,
    ) as should_proceed:
        if should_proceed:
            if booking_status := TicketStatusAdapter.to_booking_status(payload.status):
                await repository.create(
                    BookingCreateDB(
                        session_id=payload.session_id,
                        seat_id=payload.seat_id,
                        status=booking_status,
                    )
                )


@fs_router.subscriber(
    "purchases.tickets.bulk.created",
    stream=purchases_stream,
    pull_sub=True,
    durable=BookingDurables.SESSION_SVC_TICKETS_BULK_CREATED_BOOKINGS_CREATE,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def tickets_created_on_order_microservice_bookings_create(
        payload: list[TicketCreateEvent],
        repository: FromDishka[BookingRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=BookingDurables.SESSION_SVC_TICKETS_BULK_CREATED_BOOKINGS_CREATE,
    ) as should_proceed:
        if should_proceed:
            bookings_to_create: list[BookingCreateDB] = []

            for ticket in payload:
                booking_status = TicketStatusAdapter.to_booking_status(ticket.status)
                if booking_status is not None:
                    bookings_to_create.append(
                        BookingCreateDB(
                            session_id=ticket.session_id,
                            seat_id=ticket.seat_id,
                            status=booking_status,
                        )
                    )

            if bookings_to_create:
                await repository.bulk_create(bookings_to_create)


@fs_router.subscriber(
    "purchases.tickets.updated",
    stream=purchases_stream,
    pull_sub=True,
    durable=BookingDurables.SESSION_SVC_TICKETS_UPDATED_BOOKING_SYNC,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def ticket_updated_on_order_microservice_booking_sync(
        payload: TicketUpdateEvent,
        repository: FromDishka[BookingRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=BookingDurables.SESSION_SVC_TICKETS_UPDATED_BOOKING_SYNC,
    ) as should_proceed:
        if should_proceed:
            if booking_status := TicketStatusAdapter.to_booking_status(payload.status):
                await repository.upsert_status(
                    BookingCreateDB(
                        session_id=payload.session_id,
                        seat_id=payload.seat_id,
                        status=booking_status,
                    )
                )
            else:
                await repository.delete_by_session_and_seat(
                    BookingDeleteDB(
                        session_id=payload.session_id,
                        seat_id=payload.seat_id,
                    )
                )


@fs_router.subscriber(
    "purchases.tickets.bulk.updated",
    stream=purchases_stream,
    pull_sub=True,
    durable=BookingDurables.SESSION_SVC_TICKETS_BULK_UPDATED_BOOKINGS_SYNC,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def tickets_bulk_updated_on_order_microservice_sync(
        payload: list[TicketUpdateEvent],
        repository: FromDishka[BookingRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=BookingDurables.SESSION_SVC_TICKETS_BULK_UPDATED_BOOKINGS_SYNC,
    ) as should_proceed:
        if should_proceed:
            bookings_to_delete: list[BookingDeleteDB] = []
            bookings_to_upsert: list[BookingCreateDB] = []

            for ticket in payload:
                booking_status = TicketStatusAdapter.to_booking_status(ticket.status)

                if booking_status is None:
                    bookings_to_delete.append(
                        BookingDeleteDB(
                            session_id=ticket.session_id,
                            seat_id=ticket.seat_id,
                        )
                    )
                else:
                    bookings_to_upsert.append(
                        BookingCreateDB(
                            session_id=ticket.session_id,
                            seat_id=ticket.seat_id,
                            status=booking_status,
                        )
                    )

            if bookings_to_delete:
                await repository.bulk_delete_by_session_and_seat(bookings_to_delete)

            if bookings_to_upsert:
                await repository.bulk_upsert_status(bookings_to_upsert)


@fs_router.subscriber(
    "purchases.tickets.deleted",
    stream=purchases_stream,
    pull_sub=True,
    durable=BookingDurables.SESSION_SVC_TICKET_DELETED_BOOKING_DELETE,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def ticket_deleted_on_order_microservice_booking_delete(
        payload: TicketDeleteEvent,
        repository: FromDishka[BookingRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=BookingDurables.SESSION_SVC_TICKET_DELETED_BOOKING_DELETE,
    ) as should_proceed:
        if should_proceed:
            await repository.delete_by_session_and_seat(
                BookingDeleteDB(**payload.model_dump())
            )
