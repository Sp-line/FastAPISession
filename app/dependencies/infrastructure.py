from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide, alias
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from events.event_session import EventSession


class InfrastructureProvider(Provider):
    session_alias = alias(source=EventSession, provides=AsyncSession)

    @provide(scope=Scope.REQUEST)
    async def get_db_session(self) -> AsyncGenerator[EventSession, None]:
        async with db_helper.session_factory() as session:
            yield session
