from dishka import Provider, Scope, provide

from services import (
    AddressService,
    CinemaService,
    HallService,
    SessionService,
    BookingService,
    MovieService,
    SeatService,
    SessionPriceService
)


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
