from dishka import Provider, Scope, provide

from services.address import AddressService
from services.booking import BookingService
from services.cinema import CinemaService
from services.hall import HallService
from services.movie import MovieService
from services.seat import SeatService
from services.session import SessionService
from services.session_price import SessionPriceService


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    get_address_service = provide(AddressService)
    get_cinema_service = provide(CinemaService)
    get_hall_service = provide(HallService)
    get_session_service = provide(SessionService)
    get_booking_service = provide(BookingService)
    get_movie_service = provide(MovieService)
    get_seat_service = provide(SeatService)
    get_session_price_service = provide(SessionPriceService)
