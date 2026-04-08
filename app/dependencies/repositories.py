from dishka import Provider, Scope, provide

from repositories import (
    UnitOfWork,
    AddressRepository,
    CinemaRepository,
    HallRepository,
    SessionRepository,
    BookingRepository,
    MovieRepository,
    SeatRepository,
    SessionPriceRepository,
    InboxEventRepository
)


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    get_unit_of_work = provide(UnitOfWork)

    get_address_repo = provide(AddressRepository)
    get_cinema_repo = provide(CinemaRepository)
    get_hall_repo = provide(HallRepository)
    get_session_repo = provide(SessionRepository)
    get_booking_repo = provide(BookingRepository)
    get_movie_repo = provide(MovieRepository)
    get_seat_repo = provide(SeatRepository)
    get_session_price_repo = provide(SessionPriceRepository)
    get_inbox_event_repo = provide(InboxEventRepository)
