from core import fs_router
from schemas.base import Id

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
