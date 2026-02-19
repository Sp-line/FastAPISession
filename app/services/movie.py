from slugify import slugify

from repositories.movie import MovieRepository
from repositories.unit_of_work import UnitOfWork
from schemas.movie import MovieRead, MovieCreateReq, MovieUpdateReq, MovieCreateDB, MovieUpdateDB
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

    @staticmethod
    def _prepare_create_data(data: MovieCreateReq) -> MovieCreateDB:
        return MovieCreateDB(
            **data.model_dump(),
            slug=slugify(data.title)
        )

    @staticmethod
    def _prepare_update_data(data: MovieUpdateReq) -> MovieUpdateDB:
        return MovieUpdateDB(**data.model_dump(exclude_unset=True))