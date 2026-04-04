from slugify import slugify

from repositories.hall import HallRepository
from repositories.unit_of_work import UnitOfWork
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
            read_schema_type=HallRead,
        )

    @staticmethod
    def _prepare_create_data(data: HallCreateReq) -> HallCreateDB:
        return HallCreateDB(
            **data.model_dump(),
            slug=slugify(data.name)
        )

    @staticmethod
    def _prepare_update_data(data: HallUpdateReq) -> HallUpdateDB:
        return HallUpdateDB(**data.model_dump(exclude_unset=True))
