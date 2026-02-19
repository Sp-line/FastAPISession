from repositories.address import AddressRepository
from repositories.unit_of_work import UnitOfWork
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
            read_schema_type=AddressRead,
        )

    @staticmethod
    def _prepare_create_data(data: AddressCreateReq) -> AddressCreateDB:
        return AddressCreateDB(**data.model_dump())

    @staticmethod
    def _prepare_update_data(data: AddressUpdateReq) -> AddressUpdateDB:
        return AddressUpdateDB(**data.model_dump(exclude_unset=True))
