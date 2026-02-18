from constants.db import PostgresErrorCode
from exceptions.db import RelatedObjectNotFoundException, UniqueException, DeleteConstraintException
from integrity_handler.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_seats_hall_id_row_label_column_label = ConstraintRule(
    name="uq_seats_hall_id_row_label_column_label",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "seats",
        "hall_id",
        "row_label",
        "column_label"
    )
)

uq_seats_hall_id_row_column = ConstraintRule(
    name="uq_seats_hall_id_row_column",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "seats",
        "hall_id",
        "row",
        "column"
    )
)

fk_seats_hall_id_halls = ConstraintRule(
    name="fk_seats_hall_id_halls",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="hall_id",
        table_name="seats"
    )
)

fk_bookings_seat_id_seats = ConstraintRule(
    name="fk_bookings_seat_id_seats",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=DeleteConstraintException(
        table_name="seats",
        referencing_table="bookings"
    )
)

seat_error_handler = TableErrorHandler(
    uq_seats_hall_id_row_label_column_label,
    uq_seats_hall_id_row_column,
    fk_seats_hall_id_halls,
    fk_bookings_seat_id_seats
)
