from repositories import AddressRepository, UnitOfWork
from schemas.address import AddressRead, AddressCreateReq, AddressUpdateReq, AddressCreateDB, AddressUpdateDB
from services.base import ServiceBase


class AddressService(
    ServiceBase[
        AddressRepository,
        AddressRead,
        AddressCreateReq,
        AddressUpdateReq,
        AddressCreateDB,
        AddressUpdateDB,
    ],
):
    def __init__(self, repository: AddressRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="addresses",
            read_schema=AddressRead,
            db_create_schema=AddressCreateDB,
            db_update_schema=AddressUpdateDB,
        )
