from core import fs_router
from schemas.base import Id
from schemas.event import CRUDEventPublishers
from schemas.session import SessionCreateEvent, SessionUpdateEvent

session_created = fs_router.publisher(
    "showtimes.sessions.created",
    schema=SessionCreateEvent,
)

session_bulk_created = fs_router.publisher(
    "showtimes.sessions.bulk.created",
    schema=list[SessionCreateEvent],
)

session_updated = fs_router.publisher(
    "showtimes.sessions.updated",
    schema=SessionUpdateEvent,
)

session_bulk_updated = fs_router.publisher(
    "showtimes.sessions.bulk.updated",
    schema=list[SessionUpdateEvent],
)

session_deleted = fs_router.publisher(
    "showtimes.sessions.deleted",
    schema=Id,
)

session_crud_publishers = CRUDEventPublishers(
    create_pub=session_created,
    bulk_create_pub=session_bulk_created,
    update_pub=session_updated,
    bulk_update_pub=session_bulk_updated,
    delete_pub=session_deleted,
)
