from collections.abc import Iterable

from slugify import slugify

from repositories import CinemaRepository, UnitOfWork
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
            read_schema=CinemaRead,
            db_create_schema=CinemaCreateDB,
            db_update_schema=CinemaUpdateDB,
        )

    def _create_data_transfer(self, data: CinemaCreateReq) -> CinemaCreateDB:
        return self._db_create_schema(
            **data.model_dump(),
            slug=slugify(data.name),
        )

    def _bulk_create_data_transfer(self, data: Iterable[CinemaCreateReq]) -> list[CinemaCreateDB]:
        return [
            self._db_create_schema(
                **obj.model_dump(),
                slug=slugify(obj.name),
            ) for obj in data
        ]
