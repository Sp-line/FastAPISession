from repositories.seat import SeatRepository
from repositories.unit_of_work import UnitOfWork
from schemas.seat import SeatRead, SeatCreateReq, SeatUpdateReq, SeatCreateDB, SeatUpdateDB
from services.base import ServiceBase


class SeatService(
    ServiceBase[
        SeatRepository,
        SeatRead,
        SeatCreateReq,
        SeatUpdateReq,
        SeatCreateDB,
        SeatUpdateDB,
    ],
):
    def __init__(self, repository: SeatRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="seats",
            read_schema_type=SeatRead,
        )

    @staticmethod
    def _prepare_create_data(data: SeatCreateReq) -> SeatCreateDB:
        return SeatCreateDB(**data.model_dump())

    @staticmethod
    def _prepare_update_data(data: SeatUpdateReq) -> SeatUpdateDB:
        return SeatUpdateDB(**data.model_dump(exclude_unset=True))