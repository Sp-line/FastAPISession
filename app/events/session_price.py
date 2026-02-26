from core import fs_router
from schemas.base import Id
from schemas.event import CRUDEventPublishers
from schemas.session_price import SessionPriceCreateEvent, SessionPriceUpdateEvent

session_price_created = fs_router.publisher(
    "showtimes.session.prices.created",
    schema=SessionPriceCreateEvent,
)

session_price_bulk_created = fs_router.publisher(
    "showtimes.session.prices.bulk.created",
    schema=list[SessionPriceCreateEvent],
)

session_price_updated = fs_router.publisher(
    "showtimes.session.prices.updated",
    schema=SessionPriceUpdateEvent,
)

session_price_deleted = fs_router.publisher(
    "showtimes.session.prices.deleted",
    schema=Id,
)

session_price_crud_publishers = CRUDEventPublishers(
    create_pub=session_price_created,
    bulk_create_pub=session_price_bulk_created,
    update_pub=session_price_updated,
    delete_pub=session_price_deleted,
)
