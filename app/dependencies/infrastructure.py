from typing import AsyncIterable

from dishka import Provider, Scope, provide, alias
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from events.session import EventSession


class InfrastructureProvider(Provider):
    session_alias = alias(source=EventSession, provides=AsyncSession)

    @provide(scope=Scope.REQUEST)
    async def get_db_session(self) -> AsyncIterable[EventSession]:
        async with db_helper.session_factory() as session:
            yield session
