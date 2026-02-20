from datetime import date

from slugify import slugify

from repositories.movie import MovieRepository
from repositories.unit_of_work import UnitOfWork
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
            read_schema_type=MovieRead,
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

    @staticmethod
    def _prepare_create_data(data: MovieCreateReq) -> MovieCreateDB:
        return MovieCreateDB(
            **data.model_dump(),
            slug=slugify(data.title)
        )

    @staticmethod
    def _prepare_update_data(data: MovieUpdateReq) -> MovieUpdateDB:
        return MovieUpdateDB(**data.model_dump(exclude_unset=True))
