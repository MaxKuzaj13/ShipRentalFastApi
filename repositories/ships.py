from sqlalchemy.orm import Session
from models import Ship


def create(db: Session, name: str, price_per_hour: float, max_speed: int, max_range: int, available: bool):
    db_ship = Ship(name=name, price_per_hour=price_per_hour, max_speed=max_speed, max_range=max_range, available=available)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship

def fetch_one(db: Session, ship_id: int):
    return db.get(Ship, ship_id)