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
    def check_if_username_or_password_exist(db: Session, username: str, type_str: str):
        user_model = User
        column_to_query = getattr(user_model, type_str)
        unique_value = set(username[0] for username in db.query(column_to_query).all())
        return username in unique_value

    @staticmethod
    def check_word_in_file(provided_password):
        # TODO change to db table or find some better source or password_strength
        file_path_password = 'static_file/10k-most-common.txt'
        try:
            with open(file_path_password, 'r') as file:
                # Read the entire content of the file
                content = file.read()
                # Check if the word exists in the file content
                if provided_password.lower() in content:
                    return True
                else:
                    return False
        except FileNotFoundError:
            print("File with password not found.")
            return False


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
