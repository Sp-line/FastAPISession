"""add index for Hall model cinema_id fk

Revision ID: 062dd460f667
Revises: d22adeec99f0
Create Date: 2026-02-21 21:21:26.267883

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "062dd460f667"
down_revision: Union[str, None] = "d22adeec99f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        op.f("ix_halls_cinema_id"), "halls", ["cinema_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_halls_cinema_id"), table_name="halls")
