"""add Cinema model

Revision ID: fd2de03375ce
Revises:
Create Date: 2026-02-16 20:08:21.805216

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fd2de03375ce"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cinemas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cinemas")),
        sa.UniqueConstraint("slug", name=op.f("uq_cinemas_slug")),
    )


def downgrade() -> None:
    op.drop_table("cinemas")
