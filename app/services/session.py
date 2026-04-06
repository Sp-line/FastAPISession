from exceptions.db import ObjectNotFoundException
from repositories import SessionRepository, UnitOfWork
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
            read_schema=SessionRead,
            db_create_schema=SessionCreateDB,
            db_update_schema=SessionUpdateDB,
        )

    async def get_for_detail(self, obj_id: int) -> SessionDetail:
        if not (obj := await self._repository.get_for_detail(obj_id)):
            raise ObjectNotFoundException(obj_id, self._table_name)
        return SessionDetail.model_validate(obj)
