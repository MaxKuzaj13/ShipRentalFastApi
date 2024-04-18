from sqlalchemy.orm import Session
from typing import Optional, List

from models import User, Booking, Ship
from repositories.common import Repository


class UserRepository(Repository):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def get_user_by_identifier(db: Session, identifier: str) -> Optional[User]:
        """
        Fetches a user by either username or email.

        :param db: Database session
        :type db: sqlalchemy.orm.Session
        :param identifier: Username or email of the user
        :type identifier: str
        :return: User object if found, otherwise None
        :rtype: Optional[User]
        """
        return db.query(User).filter((User.username == identifier) | (User.email == identifier)).first()

    @staticmethod
    def create_booking_by_user(db: Session, user_model: User, booking: Booking) -> Booking:
        """
        Creates a booking for a given user.

        :param db: Database session
        :type db: sqlalchemy.orm.Session
        :param user_model: User model
        :type user_model: User
        :param booking: Booking details
        :type booking: Booking
        :return: Created booking
        :rtype: Booking
        """
        new_booking = Booking(
            ship_id=booking.ship_id,
            user_id=user_model.id,
            date_start=booking.date_start,
            date_end=booking.date_end
        )
        user_model.bookings.append(new_booking)
        db.add(user_model)
        db.commit()
        db.refresh(new_booking)
        return new_booking

    @staticmethod
    def get_user_bookings(db: Session, user_id: int):
        """
        Retrieves all bookings associated with a given user.

        :param db: Database session
        :type db: sqlalchemy.orm.Session
        :param user_id: ID of the user
        :type user_id: int
        :return: List of user's bookings
        :rtype:
        """
        return (
            db.query(Booking, Ship, User)
            .join(Ship, Booking.ship_id == Ship.id)
            .join(User, Booking.user_id == User.id)
            .filter(Booking.user_id == user_id)
            .all()
        )


user_repo = UserRepository()
