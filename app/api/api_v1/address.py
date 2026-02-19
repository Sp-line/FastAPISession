from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from schemas.address import AddressRead, AddressCreateReq, AddressUpdateReq
from services.address import AddressService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_addresses(service: FromDishka[AddressService], skip: int = 0, limit: int = 100) -> list[AddressRead]:
    return await service.get_all(skip, limit)


@router.get("/{address_id}")
async def get_address(address_id: int, service: FromDishka[AddressService]) -> AddressRead:
    return await service.get_by_id(address_id)


@router.post("/")
async def create_address(data: AddressCreateReq, service: FromDishka[AddressService]) -> AddressRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_addresses(data: list[AddressCreateReq], service: FromDishka[AddressService]) -> list[AddressRead]:
    return await service.bulk_create(data)


@router.patch("/{address_id}")
async def update_address(address_id: int, data: AddressUpdateReq, service: FromDishka[AddressService]) -> AddressRead:
    return await service.update(address_id, data)


@router.delete("/{address_id}")
async def delete_address(address_id: int, service: FromDishka[AddressService]) -> None:
    return await service.delete(address_id)
