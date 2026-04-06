from typing import Annotated

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Query

from schemas.base import Pagination
from schemas.booking import BookingUpdateReq, BookingCreateReq, BookingRead
from services.booking import BookingService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_bookings(
        service: FromDishka[BookingService],
        query: Annotated[Pagination, Query()]
) -> list[BookingRead]:
    return await service.get_all(query.skip, query.limit)


@router.get("/{booking_id}")
async def get_booking(booking_id: int, service: FromDishka[BookingService]) -> BookingRead:
    return await service.get_by_id(booking_id)


@router.post("/")
async def create_booking(data: BookingCreateReq, service: FromDishka[BookingService]) -> BookingRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_bookings(data: list[BookingCreateReq], service: FromDishka[BookingService]) -> list[BookingRead]:
    return await service.bulk_create(data)


@router.patch("/{booking_id}")
async def update_booking(booking_id: int, data: BookingUpdateReq, service: FromDishka[BookingService]) -> BookingRead:
    return await service.update(booking_id, data)


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, service: FromDishka[BookingService]) -> None:
    return await service.delete(booking_id)
