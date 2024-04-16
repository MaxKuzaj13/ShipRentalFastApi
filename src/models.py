from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
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
    # need have from_attributes as True in schemas


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    spaceship_id = Column(Integer)
    customer_id = Column(Integer)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    # need have from_attributes as True in schemas


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    document_number = Column(String)
    # need have from_attributes as True in schemas


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    full_name = Column(String)
    email = Column(String)
    active_user = Column(Boolean)
    # need have from_attributes as True in schemas
