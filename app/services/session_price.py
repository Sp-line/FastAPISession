from repositories.session_price import SessionPriceRepository
from repositories.unit_of_work import UnitOfWork
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
            read_schema_type=SessionPriceRead,
        )

    @staticmethod
    def _prepare_create_data(data: SessionPriceCreateReq) -> SessionPriceCreateDB:
        return SessionPriceCreateDB(**data.model_dump())

    @staticmethod
    def _prepare_update_data(data: SessionPriceUpdateReq) -> SessionPriceUpdateDB:
        return SessionPriceUpdateDB(**data.model_dump(exclude_unset=True))