"""add Session model

Revision ID: be9f753afa00
Revises: 0e4b0ab684ee
Create Date: 2026-02-17 17:01:00.565523

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "be9f753afa00"
down_revision: Union[str, None] = "0e4b0ab684ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dimension_format", sa.String(length=25), nullable=False),
        sa.Column("screen_technology", sa.String(length=25), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("hall_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        postgresql.ExcludeConstraint(
            (sa.column("hall_id"), "="),
            (sa.text("tstzrange(start_time, end_time, '[)')"), "&&"),
            using="gist",
            name="excl_session_hall_time_overlap",
        ),
        sa.CheckConstraint(
            "end_time > start_time",
            name=op.f("ck_sessions_ck_sessions_end_time_after_start_time"),
        ),
        sa.ForeignKeyConstraint(
            ["hall_id"],
            ["halls.id"],
            name=op.f("fk_sessions_hall_id_halls"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            name=op.f("fk_sessions_movie_id_movies"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sessions")),
    )


def downgrade() -> None:
    op.drop_table("sessions")
