from typing import Annotated

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Query

from schemas.base import Pagination
from schemas.movie import MovieRead, MovieCreateReq, MovieUpdateReq, MovieRelationsRead, \
    GetMoviesWithRelationsForListQuery
from services.movie import MovieService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_movies(
        service: FromDishka[MovieService],
        query: Annotated[Pagination, Query()]
) -> list[MovieRead]:
    return await service.get_all(query.skip, query.limit)


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
        query: Annotated[GetMoviesWithRelationsForListQuery, Query()]
) -> list[MovieRelationsRead]:
    return await service.get_movies_with_relations_for_list_by_cinema_id_and_date(
        **query.model_dump()
    )
