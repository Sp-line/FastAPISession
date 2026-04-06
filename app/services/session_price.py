from repositories import SessionPriceRepository, UnitOfWork
from schemas.session_price import SessionPriceRead, SessionPriceCreateReq, SessionPriceUpdateReq, SessionPriceCreateDB, \
    SessionPriceUpdateDB
from services.base import ServiceBase


class SessionPriceService(
    ServiceBase[
        SessionPriceRepository,
        SessionPriceRead,
        SessionPriceCreateReq,
        SessionPriceUpdateReq,
        SessionPriceCreateDB,
        SessionPriceUpdateDB,
    ],
):
    def __init__(self, repository: SessionPriceRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="session_prices",
            read_schema=SessionPriceRead,
            db_create_schema=SessionPriceCreateDB,
            db_update_schema=SessionPriceUpdateDB,
        )
