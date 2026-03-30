from constants import TicketStatus, BookingStatus


class TicketStatusAdapter:
    @staticmethod
    def to_booking_status(ticket_status: TicketStatus) -> BookingStatus | None:
        if ticket_status == TicketStatus.RESERVED:
            return BookingStatus.RESERVED

        if ticket_status in {TicketStatus.PAID, TicketStatus.USED, TicketStatus.REFUND_PENDING}:
            return BookingStatus.PAID

        if ticket_status in {TicketStatus.EXPIRED, TicketStatus.REFUNDED, TicketStatus.CANCELLED}:
            return None

        raise ValueError(f"Unsupported ticket status for mapping: {ticket_status}")
