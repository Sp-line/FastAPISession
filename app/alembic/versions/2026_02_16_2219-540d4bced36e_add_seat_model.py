"""add Seat model

Revision ID: 540d4bced36e
Revises: 48e015eee5e4
Create Date: 2026-02-16 22:19:32.209403

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "540d4bced36e"
down_revision: Union[str, None] = "48e015eee5e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "seats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("type", sa.String(length=30), nullable=False),
        sa.Column("row_label", sa.String(length=10), nullable=False),
        sa.Column("column_label", sa.String(length=10), nullable=False),
        sa.Column("row", sa.Integer(), nullable=False),
        sa.Column("column", sa.Integer(), nullable=False),
        sa.Column("hall_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hall_id"],
            ["halls.id"],
            name=op.f("fk_seats_hall_id_halls"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_seats")),
        sa.UniqueConstraint(
            "hall_id", "row", "column", name="uq_seats_hall_id_row_column"
        ),
        sa.UniqueConstraint(
            "hall_id",
            "row_label",
            "column_label",
            name="uq_seats_hall_id_row_label_column_label",
        ),
    )


def downgrade() -> None:
    op.drop_table("seats")
