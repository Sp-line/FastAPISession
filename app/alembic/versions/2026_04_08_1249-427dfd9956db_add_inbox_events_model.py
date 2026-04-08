"""add inbox events model

Revision ID: 427dfd9956db
Revises: 14af47754100
Create Date: 2026-04-08 12:49:55.875581

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "427dfd9956db"
down_revision: Union[str, None] = "14af47754100"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inbox_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.UUID(), nullable=False),
        sa.Column("handler", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_inbox_events")),
        sa.UniqueConstraint(
            "code", "handler", name="uq_inbox_events_code_handler"
        ),
    )


def downgrade() -> None:
    op.drop_table("inbox_events")
