"""add SessionPrice model

Revision ID: 582fccd16581
Revises: be9f753afa00
Create Date: 2026-02-17 20:43:50.321794

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "582fccd16581"
down_revision: Union[str, None] = "be9f753afa00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "session_prices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("seat_type", sa.String(length=30), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
            name=op.f("fk_session_prices_session_id_sessions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_session_prices")),
        sa.UniqueConstraint(
            "session_id",
            "seat_type",
            name="uq_session_prices_session_id_seat_type",
        ),
    )


def downgrade() -> None:
    op.drop_table("session_prices")
