from slugify import slugify

from repositories.cinema import CinemaRepository
from repositories.unit_of_work import UnitOfWork
from schemas.cinema import CinemaRead, CinemaCreateReq, CinemaUpdateReq, CinemaCreateDB, CinemaUpdateDB
from services.base import ServiceBase


class CinemaService(
    ServiceBase[
        CinemaRepository,
        CinemaRead,
        CinemaCreateReq,
        CinemaUpdateReq,
        CinemaCreateDB,
        CinemaUpdateDB,
    ],
):
    def __init__(self, repository: CinemaRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="cinemas",
            read_schema_type=CinemaRead,
        )

    @staticmethod
    def _prepare_create_data(data: CinemaCreateReq) -> CinemaCreateDB:
        return CinemaCreateDB(
            **data.model_dump(),
            slug=slugify(data.name)
        )

    @staticmethod
    def _prepare_update_data(data: CinemaUpdateReq) -> CinemaUpdateDB:
        return CinemaUpdateDB(**data.model_dump(exclude_unset=True))
