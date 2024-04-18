from sqlalchemy.orm import Session
from typing import Optional, List, Tuple

from models import User, Booking, Ship
from repositories.common import Repository


class UserRepository(Repository):
    def __init__(self):
        """
        Initializes a UserRepository instance.
        """
        super().__init__(User)

    @staticmethod
    def get_user_by_identifier(db: Session, identifier: str) -> Optional[User]:
        """
        Fetches a user by either username or email.

        Args:
            db (Session): Database session
            identifier (str): Username or email of the user

        Returns:
            Optional[User]: User object if found, otherwise None
        """
        return db.query(User).filter((User.username == identifier) | (User.email == identifier)).first()

    @staticmethod
    def create_booking_by_user(db: Session, user_model: User, booking: Booking) -> Booking:
        """
        Creates a booking for a given user.

        Args:
            db (Session): Database session
            user_model (User): User model
            booking (Booking): Booking details

        Returns:
            Booking: Created booking
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
    def get_user_bookings(db: Session, user_id: int) -> List[Tuple[Booking, Ship, User]]:
        """
        Retrieves all bookings associated with a given user.

        Args:
            db (Session): Database session
            user_id (int): ID of the user

        Returns:
            List[Tuple[Booking, Ship, User]]: List of user's bookings
        """
        return (
            db.query(Booking, Ship, User)
            .join(Ship, Booking.ship_id == Ship.id)
            .join(User, Booking.user_id == User.id)
            .filter(Booking.user_id == user_id)
            .all()
        )


user_repo = UserRepository()
