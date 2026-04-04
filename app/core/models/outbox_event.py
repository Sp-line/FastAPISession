import uuid
from typing import Any

from sqlalchemy import UUID, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped

from constants import OutboxEventLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin
from core.models.mixins.observable import ObservableMixin


class OutboxEvent(IntIdPkMixin, ObservableMixin, Base):
    code: Mapped[uuid.UUID] = mapped_column(
        UUID,
        default=uuid.uuid4,
        unique=True,
    )
    subject: Mapped[str] = mapped_column(String(OutboxEventLimits.SUBJECT_MAX))
    payload: Mapped[dict[str, Any] | list[Any]] = mapped_column(JSONB)
