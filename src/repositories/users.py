from sqlalchemy.orm import Session
from typing import Optional

from models import User, Booking, Ship
from repositories.common import Repository


class UserRepository(Repository):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def get_user_by_identifier(db: Session, identifier: str):
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
    def create_booking_by_user(db: Session, user_model: User, booking: Booking):
        booking = Booking(
            ship_id=booking.ship_id,
            user_id=user_model.id,
            date_start=booking.date_start,
            date_end=booking.date_end
        )
        user_model.bookings.append(booking)
        db.add(user_model)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def get_user_bookings(db: Session, user_id: int):
        return (
            db.query(Booking)
            .join(Booking.ship)
            .join(Booking.user)
            .filter(Booking.user_id == user_id)
            .all()
        )

    # @staticmethod
    # def get_user_bookings(db: Session, user_model: User, booking: Booking):
    #     booking = Booking(
    #         spaceship_id=booking.spaceship_id,
    #         customer_id=user_model.id,
    #         date_start=booking.date_start,
    #         date_end=booking.date_end
    #     )
    #     # use one not first to have handle exception lack of user and 2 user with same name
    #
    #     # user_model = db.query(User).filter(User.id == user_id).one()
    #     # user_model.bookings.append(booking)
    #     # db.add(user_model)
    #     # db.commit()




user_repo = UserRepository()
