from core import fs_router
from schemas.event import CRUDEventPublishers
from schemas.hall import HallCreateEvent, HallUpdateEvent, Id

hall_created = fs_router.publisher(
    "showtimes.halls.created",
    schema=HallCreateEvent,
)

hall_bulk_created = fs_router.publisher(
    "showtimes.halls.bulk.created",
    schema=list[HallCreateEvent],
)

hall_updated = fs_router.publisher(
    "showtimes.halls.updated",
    schema=HallUpdateEvent,
)

hall_bulk_updated = fs_router.publisher(
    "showtimes.halls.bulk.updated",
    schema=list[HallUpdateEvent],
)

hall_deleted = fs_router.publisher(
    "showtimes.halls.deleted",
    schema=Id,
)

hall_crud_publishers = CRUDEventPublishers(
    create_pub=hall_created,
    bulk_create_pub=hall_bulk_created,
    update_pub=hall_updated,
    bulk_update_pub=hall_bulk_updated,
    delete_pub=hall_deleted,
)
