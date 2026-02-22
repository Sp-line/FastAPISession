from constants.db import PostgresErrorCode
from exceptions.db import RelatedObjectNotFoundException, DeleteConstraintException, ExclusionException, \
    CheckConstraintException
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

excl_session_hall_time_overlap = ConstraintRule(
    name="excl_session_hall_time_overlap",
    error_code=PostgresErrorCode.EXCLUSION_VIOLATION,
    exception=ExclusionException(
        "sessions",
        "start_time", "end_time"
    )
)

ck_sessions_end_time_after_start_time = ConstraintRule(
    name="ck_sessions_end_time_after_start_time",
    error_code=PostgresErrorCode.CHECK_VIOLATION,
    exception=CheckConstraintException(
        table_name="sessions",
        expression="end_time > start_time"
    )
)

session_error_handler = TableErrorHandler(
    ck_sessions_end_time_after_start_time,
    excl_session_hall_time_overlap,
    fk_sessions_hall_id_halls,
    fk_sessions_movie_id_movies,
    fk_bookings_session_id_sessions_delete
)
