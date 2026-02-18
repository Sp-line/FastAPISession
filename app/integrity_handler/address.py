from constants.db import PostgresErrorCode
from exceptions.db import UniqueFieldException, RelatedObjectNotFoundException, DeleteConstraintException
from integrity_handler.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_addresses_cinema_id = ConstraintRule(
    name="uq_addresses_cinema_id",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="cinema_id",
        table_name="addresses"
    )
)

fk_addresses_cinema_id_cinemas = ConstraintRule(
    name="fk_addresses_cinema_id_cinemas",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="cinema_id",
        table_name="addresses"
    )
)

address_error_handler = TableErrorHandler(
    uq_addresses_cinema_id,
    fk_addresses_cinema_id_cinemas,
)
