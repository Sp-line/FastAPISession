from core import fs_router
from schemas.event import CRUDEventPublishers
from schemas.seat import SeatCreateEvent, SeatUpdateEvent, SeatDeleteEvent

seat_created = fs_router.publisher(
    "showtimes.seats.created",
    schema=SeatCreateEvent,
)

seat_bulk_created = fs_router.publisher(
    "showtimes.seats.bulk.created",
    schema=list[SeatCreateEvent],
)

seat_updated = fs_router.publisher(
    "showtimes.seats.updated",
    schema=SeatUpdateEvent,
)

seat_deleted = fs_router.publisher(
    "showtimes.seats.deleted",
    schema=SeatDeleteEvent,
)

seat_crud_publishers = CRUDEventPublishers(
    create_pub=seat_created,
    bulk_create_pub=seat_bulk_created,
    update_pub=seat_updated,
    delete_pub=seat_deleted,
)
