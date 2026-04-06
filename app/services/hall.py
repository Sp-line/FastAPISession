from collections.abc import Iterable

from slugify import slugify

from repositories import HallRepository, UnitOfWork
from schemas.hall import HallRead, HallCreateReq, HallUpdateReq, HallCreateDB, HallUpdateDB
from services.base import ServiceBase


class HallService(
    ServiceBase[
        HallRepository,
        HallRead,
        HallCreateReq,
        HallUpdateReq,
        HallCreateDB,
        HallUpdateDB,
    ],
):
    def __init__(self, repository: HallRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="halls",
            read_schema=HallRead,
            db_create_schema=HallCreateDB,
            db_update_schema=HallUpdateDB,
        )

    def _create_data_transfer(self, data: HallCreateReq) -> HallCreateDB:
        return self._db_create_schema(
            **data.model_dump(),
            slug=slugify(data.name),
        )

    def _bulk_create_data_transfer(self, data: Iterable[HallCreateReq]) -> list[HallCreateDB]:
        return [
            self._db_create_schema(
                **obj.model_dump(),
                slug=slugify(obj.name),
            ) for obj in data
        ]
