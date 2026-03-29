from enum import StrEnum


class BookingLimits:
    STATUS_MAX: int = 30


class BookingStatus(StrEnum):
    PAID = "paid"
    RESERVED = "reserved"
