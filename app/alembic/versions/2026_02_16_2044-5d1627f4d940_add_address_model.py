"""add Address model

Revision ID: 5d1627f4d940
Revises: fd2de03375ce
Create Date: 2026-02-16 20:44:14.449293

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "5d1627f4d940"
down_revision: Union[str, None] = "fd2de03375ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("street", sa.String(length=100), nullable=False),
        sa.Column("house_number", sa.String(length=20), nullable=False),
        sa.Column("zip_code", sa.String(length=20), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("cinema_id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "latitude >= -90 AND latitude <= 90",
            name=op.f("ck_addresses_check_latitude_range"),
        ),
        sa.CheckConstraint(
            "longitude >= -180 AND longitude <= 180",
            name=op.f("ck_addresses_check_longitude_range"),
        ),
        sa.ForeignKeyConstraint(
            ["cinema_id"],
            ["cinemas.id"],
            name=op.f("fk_addresses_cinema_id_cinemas"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_addresses")),
        sa.UniqueConstraint("cinema_id", name=op.f("uq_addresses_cinema_id")),
    )


def downgrade() -> None:
    op.drop_table("addresses")
