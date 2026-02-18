from constants.db import PostgresErrorCode
from exceptions.db import UniqueFieldException, UniqueException, RelatedObjectNotFoundException, \
    DeleteConstraintException
from integrity_handler.base import TableErrorHandler
from schemas.db import ConstraintRule

fk_halls_cinema_id_cinemas = ConstraintRule(
    name="fk_halls_cinema_id_cinemas",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="cinema_id",
        table_name="halls"
    )
)

uq_halls_slug = ConstraintRule(
    name="uq_halls_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="halls"
    )
)

uq_halls_cinema_id_name = ConstraintRule(
    name="uq_halls_cinema_id_name",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "halls",
        "cinema_id", "name"
    )
)

fk_sessions_hall_id_halls_delete = ConstraintRule(
    name="fk_sessions_hall_id_halls",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="halls",
        referencing_table="sessions"
    )
)

hall_error_handler = TableErrorHandler(
    uq_halls_slug,
    uq_halls_cinema_id_name,
    fk_halls_cinema_id_cinemas,
    fk_sessions_hall_id_halls_delete
)
