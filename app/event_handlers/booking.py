from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy

from core import fs_router, purchases_stream
from event_handlers.base import base_consumer_config
from repositories import BookingRepository, UnitOfWork
from schemas.booking import BookingCreateDB, BookingDeleteDB
from schemas.ticket import TicketCreateEvent, TicketUpdateEvent, TicketDeleteEvent
from services.ticket import TicketStatusAdapter


@fs_router.subscriber(
    "purchases.tickets.created",
    stream=purchases_stream,
    pull_sub=True,
    durable="order_svc_tickets_created_booking_create",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def ticket_created_on_order_microservice_booking_create(
        payload: TicketCreateEvent,
        repository: FromDishka[BookingRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    booking_status = TicketStatusAdapter.to_booking_status(payload.status)
    if booking_status is None:
        return

    async with unit_of_work:
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
    durable="order_svc_tickets_bulk_created_bookings_create",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def tickets_created_on_order_microservice_bookings_create(
        payload: list[TicketCreateEvent],
        repository: FromDishka[BookingRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    bookings_to_create: list[BookingCreateDB] = []

    for ticket in payload:
        booking_status = TicketStatusAdapter.to_booking_status(ticket.status)
        if booking_status is None:
            continue

        bookings_to_create.append(
            BookingCreateDB(
                session_id=ticket.session_id,
                seat_id=ticket.seat_id,
                status=booking_status,
            )
        )

    if bookings_to_create:
        async with unit_of_work:
            await repository.bulk_create(bookings_to_create)


@fs_router.subscriber(
    "purchases.tickets.updated",
    stream=purchases_stream,
    pull_sub=True,
    durable="order_svc_tickets_updated_booking_sync",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def ticket_updated_on_order_microservice_booking_sync(
        payload: TicketUpdateEvent,
        repository: FromDishka[BookingRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    booking_status = TicketStatusAdapter.to_booking_status(payload.status)

    async with unit_of_work:
        if booking_status is None:
            await repository.delete_by_session_and_seat(
                BookingDeleteDB(
                    session_id=payload.session_id,
                    seat_id=payload.seat_id,
                )
            )
        else:
            await repository.upsert_status(
                BookingCreateDB(
                    session_id=payload.session_id,
                    seat_id=payload.seat_id,
                    status=booking_status,
                )
            )


@fs_router.subscriber(
    "purchases.tickets.bulk.updated",
    stream=purchases_stream,
    pull_sub=True,
    durable="order_svc_tickets_bulk_updated_bookings_sync",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def tickets_bulk_updated_on_order_microservice_sync(
        payload: list[TicketUpdateEvent],
        repository: FromDishka[BookingRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
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

    if bookings_to_delete or bookings_to_upsert:
        async with unit_of_work:
            if bookings_to_delete:
                await repository.bulk_delete_by_session_and_seat(bookings_to_delete)

            if bookings_to_upsert:
                await repository.bulk_upsert_status(bookings_to_upsert)


@fs_router.subscriber(
    "purchases.tickets.deleted",
    stream=purchases_stream,
    pull_sub=True,
    durable="order_svc_ticket_deleted_booking_delete",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def ticket_deleted_on_order_microservice_booking_delete(
        payload: TicketDeleteEvent,
        repository: FromDishka[BookingRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.delete_by_session_and_seat(
            BookingDeleteDB(
                **payload.model_dump()
            )
        )
