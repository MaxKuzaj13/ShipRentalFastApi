from sqlalchemy.orm import Session
from sqlalchemy import update

from models import Ship


def create(db: Session, name: str, price_per_hour: float, max_speed: int, max_range: int, available: bool):
    db_ship = Ship(name=name, price_per_hour=price_per_hour, max_speed=max_speed, max_range=max_range, available=available)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship


def fetch_one(db: Session, spaceship_id: int):
    ship = db.get(Ship, spaceship_id)
    if not ship:
        return None
    return ship


def delete_one(db: Session, spaceship_id: int):
    ship = db.get(Ship, spaceship_id)
    if ship:
        db.delete(ship)
        db.commit()
        return ship
    else:
        return None


def fetch_all(db: Session):
    return db.query(Ship).all()


def update_one(db: Session, spaceship_id: int, **kwargs):
    db_ship = db.execute(update(Ship).where(Ship.id == spaceship_id).values(**kwargs))
    # Check if it is some object or is empty
    if db_ship.rowcount > 0:
        db.commit()
        updated_data = kwargs.copy()
        updated_data['id'] = spaceship_id
        return updated_data
    else:
        return None
