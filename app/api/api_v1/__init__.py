from fastapi import APIRouter

from core.config import settings
from .address import router as address_router
from .cinema import router as cinema_router
from .hall import router as hall_router
from .session import router as session_router
from .booking import router as booking_router
from .movie import router as movie_router
from .seat import router as seat_router
from .session_price import router as session_price_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(address_router, prefix="/addresses", tags=["Addresses"])
router.include_router(cinema_router, prefix="/cinemas", tags=["Cinemas"])
router.include_router(hall_router, prefix="/halls", tags=["Halls"])
router.include_router(session_router, prefix="/sessions", tags=["Sessions"])
router.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
router.include_router(movie_router, prefix="/movies", tags=["Movies"])
router.include_router(seat_router, prefix="/seats", tags=["Seats"])
router.include_router(session_price_router, prefix="/session-prices", tags=["Session-Prices"])
