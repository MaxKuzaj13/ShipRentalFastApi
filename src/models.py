from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db import Base, engine

Base.metadata.create_all(bind=engine)

class Ship(Base):
    __tablename__ = 'ships'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price_per_hour = Column(Float)
    max_speed = Column(Integer)
    max_range = Column(Integer)
    available = Column(Boolean)
    bookings = relationship("Booking", back_populates='ship')

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    ship_id = Column(Integer, ForeignKey('ships.id'))
    ship = relationship("Ship", back_populates='bookings')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates='bookings')

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    document_number = Column(String)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    full_name = Column(String)
    email = Column(String)
    active_user = Column(Boolean)
    bookings = relationship("Booking", back_populates='user')
