from models import Booking
from repositories.common import Repository


class BookingRepository(Repository):
    def __init__(self):
        super().__init__(Booking)


booking_repo = BookingRepository()
