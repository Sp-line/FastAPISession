"""add Hall model

Revision ID: 48e015eee5e4
Revises: 5d1627f4d940
Create Date: 2026-02-16 21:31:05.176862

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "48e015eee5e4"
down_revision: Union[str, None] = "5d1627f4d940"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "halls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("slug", sa.String(length=30), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("tech_type", sa.String(length=15), nullable=False),
        sa.Column("cinema_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cinema_id"],
            ["cinemas.id"],
            name=op.f("fk_halls_cinema_id_cinemas"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_halls")),
        sa.UniqueConstraint(
            "cinema_id", "name", name="uq_halls_cinema_id_name"
        ),
        sa.UniqueConstraint("slug", name=op.f("uq_halls_slug")),
    )


def downgrade() -> None:
    op.drop_table("halls")
