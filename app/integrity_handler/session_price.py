from constants.db import PostgresErrorCode
from exceptions.db import UniqueException, RelatedObjectNotFoundException
from integrity_handler.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_session_prices_session_id_seat_type = ConstraintRule(
    name="uq_session_prices_session_id_seat_type",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "session_prices",
        "session_id",
        "seat_type"
    )
)

fk_session_prices_session_id_sessions = ConstraintRule(
    name="fk_session_prices_session_id_sessions",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="session_id",
        table_name="session_prices"
    )
)

session_price_error_handler = TableErrorHandler(
    uq_session_prices_session_id_seat_type,
    fk_session_prices_session_id_sessions
)