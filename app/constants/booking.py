from enum import StrEnum


class BookingLimits:
    STATUS_MAX: int = 30


class SeatAvailabilityStatus(StrEnum):
    SOLD = "sold"
    RESERVED = "reserved"
