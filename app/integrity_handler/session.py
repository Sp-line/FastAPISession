from constants.db import PostgresErrorCode
from exceptions.db import RelatedObjectNotFoundException, DeleteConstraintException
from integrity_handler.base import TableErrorHandler
from schemas.db import ConstraintRule

fk_sessions_hall_id_halls = ConstraintRule(
    name="fk_sessions_hall_id_halls",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="hall_id",
        table_name="sessions"
    )
)

fk_sessions_movie_id_movies = ConstraintRule(
    name="fk_sessions_movie_id_movies",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="movie_id",
        table_name="sessions"
    )
)

fk_bookings_session_id_sessions_delete = ConstraintRule(
    name="fk_bookings_session_id_sessions",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="sessions",
        referencing_table="bookings"
    )
)

session_error_handler = TableErrorHandler(
    fk_sessions_hall_id_halls,
    fk_sessions_movie_id_movies,
    fk_bookings_session_id_sessions_delete
)
