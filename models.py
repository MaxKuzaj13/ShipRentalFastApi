from sqlalchemy import Column, Integer, String, Float, Boolean
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
