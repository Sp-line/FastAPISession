"""delete is_active fields from models

Revision ID: 544ec32c79a4
Revises: 062dd460f667
Create Date: 2026-02-21 22:54:12.211121

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "544ec32c79a4"
down_revision: Union[str, None] = "062dd460f667"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("cinemas", "is_available")
    op.drop_column("seats", "is_active")
    op.drop_column("sessions", "is_active")


def downgrade() -> None:
    op.add_column(
        "sessions",
        sa.Column(
            "is_active", sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "seats",
        sa.Column(
            "is_active", sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "cinemas",
        sa.Column(
            "is_available", sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False
        ),
    )
