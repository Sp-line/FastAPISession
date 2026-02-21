from exceptions.db import ObjectNotFoundException
from repositories.session import SessionRepository
from repositories.unit_of_work import UnitOfWork
from schemas.session import SessionRead, SessionCreateReq, SessionUpdateReq, SessionCreateDB, SessionUpdateDB, \
    SessionDetail
from services.base import ServiceBase


class SessionService(
    ServiceBase[
        SessionRepository,
        SessionRead,
        SessionCreateReq,
        SessionUpdateReq,
        SessionCreateDB,
        SessionUpdateDB,
    ],
):
    def __init__(self, repository: SessionRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="sessions",
            read_schema_type=SessionRead,
        )

    async def get_for_detail(self, obj_id: int) -> SessionDetail:
        if not (obj := await self._repository.get_for_detail(obj_id)):
            raise ObjectNotFoundException(obj_id, self._table_name)
        return SessionDetail.model_validate(obj)

    @staticmethod
    def _prepare_create_data(data: SessionCreateReq) -> SessionCreateDB:
        return SessionCreateDB(**data.model_dump())

    @staticmethod
    def _prepare_update_data(data: SessionUpdateReq) -> SessionUpdateDB:
        return SessionUpdateDB(**data.model_dump(exclude_unset=True))
