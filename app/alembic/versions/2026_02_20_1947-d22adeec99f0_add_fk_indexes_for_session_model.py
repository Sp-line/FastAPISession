"""add fk indexes for Session model

Revision ID: d22adeec99f0
Revises: 6b962d477ca9
Create Date: 2026-02-20 19:47:40.925065

"""

from typing import Sequence, Union

from alembic import op

revision: str = "d22adeec99f0"
down_revision: Union[str, None] = "6b962d477ca9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        op.f("ix_sessions_hall_id"), "sessions", ["hall_id"], unique=False
    )
    op.create_index(
        op.f("ix_sessions_movie_id"), "sessions", ["movie_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_sessions_movie_id"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_hall_id"), table_name="sessions")
