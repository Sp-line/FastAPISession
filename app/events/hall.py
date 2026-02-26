from core import fs_router
from schemas.event import CRUDEventPublishers
from schemas.seat import SeatCreateEvent, SeatUpdateEvent, SeatDeleteEvent

hall_created = fs_router.publisher(
    "showtimes.halls.created",
    schema=SeatCreateEvent,
)

hall_bulk_created = fs_router.publisher(
    "showtimes.halls.bulk.created",
    schema=list[SeatCreateEvent],
)

hall_updated = fs_router.publisher(
    "showtimes.halls.updated",
    schema=SeatUpdateEvent,
)

hall_deleted = fs_router.publisher(
    "showtimes.halls.deleted",
    schema=SeatDeleteEvent,
)

hall_crud_publishers = CRUDEventPublishers(
    create_pub=hall_created,
    bulk_create_pub=hall_bulk_created,
    update_pub=hall_updated,
    delete_pub=hall_deleted,
)
