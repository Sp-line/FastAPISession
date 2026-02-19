from repositories.booking import BookingRepository
from repositories.unit_of_work import UnitOfWork
from schemas.booking import BookingRead, BookingCreateReq, BookingUpdateReq, BookingCreateDB, BookingUpdateDB
from services.base import ServiceBase


class BookingService(
    ServiceBase[
        BookingRepository,
        BookingRead,
        BookingCreateReq,
        BookingUpdateReq,
        BookingCreateDB,
        BookingUpdateDB,
    ],
):
    def __init__(self, repository: BookingRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="bookings",
            read_schema_type=BookingRead,
        )

    @staticmethod
    def _prepare_create_data(data: BookingCreateReq) -> BookingCreateDB:
        return BookingCreateDB(**data.model_dump())

    @staticmethod
    def _prepare_update_data(data: BookingUpdateReq) -> BookingUpdateDB:
        return BookingUpdateDB(**data.model_dump(exclude_unset=True))