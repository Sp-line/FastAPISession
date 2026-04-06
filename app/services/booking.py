from repositories import BookingRepository, UnitOfWork
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
            read_schema=BookingRead,
            db_create_schema=BookingCreateDB,
            db_update_schema=BookingUpdateDB,
        )
