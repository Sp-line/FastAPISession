from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from schemas.cinema import CinemaRead, CinemaCreateReq, CinemaUpdateReq
from services.cinema import CinemaService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_cinemas(service: FromDishka[CinemaService], skip: int = 0, limit: int = 100) -> list[CinemaRead]:
    return await service.get_all(skip, limit)


@router.get("/{cinema_id}")
async def get_cinema(cinema_id: int, service: FromDishka[CinemaService]) -> CinemaRead:
    return await service.get_by_id(cinema_id)


@router.post("/")
async def create_cinema(data: CinemaCreateReq, service: FromDishka[CinemaService]) -> CinemaRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_cinemas(data: list[CinemaCreateReq], service: FromDishka[CinemaService]) -> list[CinemaRead]:
    return await service.bulk_create(data)


@router.patch("/{cinema_id}")
async def update_cinema(cinema_id: int, data: CinemaUpdateReq, service: FromDishka[CinemaService]) -> CinemaRead:
    return await service.update(cinema_id, data)


@router.delete("/{cinema_id}")
async def delete_cinema(cinema_id: int, service: FromDishka[CinemaService]) -> None:
    return await service.delete(cinema_id)
