from constants.db import PostgresErrorCode
from exceptions.db import UniqueFieldException, DeleteConstraintException
from integrity_handler.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_cinemas_slug = ConstraintRule(
    name="uq_cinemas_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="cinemas"
    )
)

fk_halls_cinema_id_cinemas = ConstraintRule(
    name="fk_halls_cinema_id_cinemas",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="cinemas",
        referencing_table="halls"
    )
)

cinema_error_handler = TableErrorHandler(
    uq_cinemas_slug,
    fk_halls_cinema_id_cinemas
)
