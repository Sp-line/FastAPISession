from enum import StrEnum


class TicketStatus(StrEnum):
    RESERVED = "reserved"
    PAID = "paid"
    USED = "used"
    EXPIRED = "expired"
    REFUND_PENDING = "refund_pending"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"
