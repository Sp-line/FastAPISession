"""add Movie model

Revision ID: 0e4b0ab684ee
Revises: 540d4bced36e
Create Date: 2026-02-17 15:54:12.781235

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0e4b0ab684ee"
down_revision: Union[str, None] = "540d4bced36e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("duration", sa.SmallInteger(), nullable=False),
        sa.Column("age_rating", sa.String(length=10), nullable=False),
        sa.Column("premiere_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("poster_url", sa.String(length=1024), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_movies")),
        sa.UniqueConstraint("slug", name=op.f("uq_movies_slug")),
    )


def downgrade() -> None:
    op.drop_table("movies")
