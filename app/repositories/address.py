from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Address
from integrity_handler import address_error_handler
from repositories.base import RepositoryBase
from schemas.address import AddressCreateDB, AddressUpdateDB


class AddressRepository(
    RepositoryBase[
        Address,
        AddressCreateDB,
        AddressUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Address,
            session=session,
            table_error_handler=address_error_handler,
        )
