from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from events.session import EventSession
from repositories.address import AddressRepository
from repositories.booking import BookingRepository
from repositories.cinema import CinemaRepository
from repositories.hall import HallRepository
from repositories.movie import MovieRepository
from repositories.seat import SeatRepository
from repositories.session import SessionRepository
from repositories.session_price import SessionPriceRepository
from repositories.signals import SignalUnitOfWork
from repositories.unit_of_work import UnitOfWork


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_uow(self, session: AsyncSession) -> UnitOfWork:
        return UnitOfWork(session)

    @provide
    def get_signal_uow(self, session: EventSession) -> SignalUnitOfWork:
        return SignalUnitOfWork(session)

    get_address_repo = provide(AddressRepository)
    get_cinema_repo = provide(CinemaRepository)
    get_hall_repo = provide(HallRepository)
    get_session_repo = provide(SessionRepository)
    get_booking_repo = provide(BookingRepository)
    get_movie_repo = provide(MovieRepository)
    get_seat_repo = provide(SeatRepository)
    get_session_price_repo = provide(SessionPriceRepository)