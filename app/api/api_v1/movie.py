from datetime import date

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from schemas.movie import MovieRead, MovieCreateReq, MovieUpdateReq, MovieRelationsRead
from services.movie import MovieService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_movies(service: FromDishka[MovieService], skip: int = 0, limit: int = 100) -> list[MovieRead]:
    return await service.get_all(skip, limit)


@router.get("/{movie_id}")
async def get_movie(movie_id: int, service: FromDishka[MovieService]) -> MovieRead:
    return await service.get_by_id(movie_id)


@router.post("/")
async def create_movie(data: MovieCreateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_movies(data: list[MovieCreateReq], service: FromDishka[MovieService]) -> list[MovieRead]:
    return await service.bulk_create(data)


@router.patch("/{movie_id}")
async def update_movie(movie_id: int, data: MovieUpdateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.update(movie_id, data)


@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, service: FromDishka[MovieService]) -> None:
    return await service.delete(movie_id)


@router.get("/relations/list")
async def get_movies_with_relations_for_list(
        service: FromDishka[MovieService],
        cinema_id: int,
        target_date: date,
        skip: int = 0,
        limit: int = 100
) -> list[MovieRelationsRead]:
    return await service.get_movies_with_relations_for_list_by_cinema_id_and_date(
        cinema_id=cinema_id,
        target_date=target_date,
        skip=skip,
        limit=limit
    )
