from collections.abc import Iterable
from datetime import date

from slugify import slugify

from repositories import MovieRepository, UnitOfWork
from schemas.movie import MovieRead, MovieCreateReq, MovieUpdateReq, MovieCreateDB, MovieUpdateDB, MovieRelationsRead
from services.base import ServiceBase


class MovieService(
    ServiceBase[
        MovieRepository,
        MovieRead,
        MovieCreateReq,
        MovieUpdateReq,
        MovieCreateDB,
        MovieUpdateDB,
    ],
):
    def __init__(self, repository: MovieRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movies",
            read_schema=MovieRead,
            db_create_schema=MovieCreateDB,
            db_update_schema=MovieUpdateDB,
        )

    async def get_movies_with_relations_for_list_by_cinema_id_and_date(
            self,
            cinema_id: int,
            target_date: date,
            skip: int = 0,
            limit: int = 100
    ) -> list[MovieRelationsRead]:
        return [
            MovieRelationsRead.model_validate(obj)
            for obj in
            await self._repository.get_movies_with_relations_for_list_by_cinema_id_and_date(
                cinema_id=cinema_id,
                target_date=target_date,
                skip=skip,
                limit=limit,
            )
        ]

    def _create_data_transfer(self, data: MovieCreateReq) -> MovieCreateDB:
        return self._db_create_schema(
            **data.model_dump(),
            slug=slugify(data.title),
        )

    def _bulk_create_data_transfer(self, data: Iterable[MovieCreateReq]) -> list[MovieCreateDB]:
        return [
            self._db_create_schema(
                **obj.model_dump(),
                slug=slugify(obj.title),
            ) for obj in data
        ]
