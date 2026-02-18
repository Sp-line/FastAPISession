from constants.db import PostgresErrorCode
from exceptions.db import RelatedObjectNotFoundException, UniqueException
from integrity_handler.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_bookings_session_id_seat_id = ConstraintRule(
    name="uq_bookings_session_id_seat_id",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "bookings",
        "session_id",
        "seat_id"
    )
)

fk_bookings_session_id_sessions = ConstraintRule(
    name="fk_bookings_session_id_sessions",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="session_id",
        table_name="bookings"
    )
)

fk_bookings_seat_id_seats = ConstraintRule(
    name="fk_bookings_seat_id_seats",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="seat_id",
        table_name="bookings"
    )
)

booking_error_handler = TableErrorHandler(
    uq_bookings_session_id_seat_id,
    fk_bookings_session_id_sessions,
    fk_bookings_seat_id_seats
)
