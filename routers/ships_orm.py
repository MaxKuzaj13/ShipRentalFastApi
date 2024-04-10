from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Dict, List


from db import get_db
from repositories.ships import create, fetch_one, delete_one, fetch_all, update_one
from schemas.ships import SpaceshipSchemaReceived, SpaceshipSchemaStored

router = APIRouter(prefix='/spaceships', tags=['spaceships'])


@router.get("/{spaceship_id}", response_model=SpaceshipSchemaStored, status_code=200)
async def get(spaceship_id: int, db: Session = Depends(get_db)):
    ships = fetch_one(db=db, spaceship_id=spaceship_id)
    if not ships:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    return ships


@router.post("/", response_model=SpaceshipSchemaStored, status_code=201)
async def add(spaceship: SpaceshipSchemaReceived, db: Session = Depends(get_db)):
    ship = create(
        db=db,
        name=spaceship.name,
        available=True,
        price_per_hour=spaceship.price_per_hour,
        max_speed=spaceship.max_speed,
        max_range=spaceship.max_range
    )
    return ship


@router.delete("/{spaceship_id}", response_model=SpaceshipSchemaStored)
async def delete_spaceship(spaceship_id: int, db: Session = Depends(get_db)):
    ship_deleted = delete_one(db, spaceship_id)
    if not ship_deleted:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    return ship_deleted


@router.get("/", response_model=List[SpaceshipSchemaStored],  status_code=200)
async def get_all(db: Session = Depends(get_db)):
    ships = fetch_all(db=db)
    if not ships:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    return ships


@router.put("/{spaceship_id}", response_model=SpaceshipSchemaStored)
async def update_one_spaceship(spaceship_id: int, spaceship: SpaceshipSchemaReceived, db: Session = Depends(get_db)):
    ships = update_one(db=db, spaceship_id=spaceship_id, **spaceship.dict())
    if not ships:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    return ships
