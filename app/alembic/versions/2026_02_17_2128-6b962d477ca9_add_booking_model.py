"""add Booking model

Revision ID: 6b962d477ca9
Revises: 582fccd16581
Create Date: 2026-02-17 21:28:06.513693

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "6b962d477ca9"
down_revision: Union[str, None] = "582fccd16581"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("seat_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["seat_id"],
            ["seats.id"],
            name=op.f("fk_bookings_seat_id_seats"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
            name=op.f("fk_bookings_session_id_sessions"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_bookings")),
        sa.UniqueConstraint(
            "session_id", "seat_id", name="uq_bookings_session_id_seat_id"
        ),
    )


def downgrade() -> None:
    op.drop_table("bookings")
