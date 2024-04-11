from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db import get_db
from repositories.ships import ship_repo
from schemas.ships import SpaceshipSchemaReceived, SpaceshipSchemaStored

router = APIRouter(prefix='/spaceships', tags=['spaceships'])


@router.post("/", response_model=SpaceshipSchemaStored, status_code=201)
async def add(spaceship: SpaceshipSchemaReceived, db: Session = Depends(get_db)):
    """
    Endpoint to add a new spaceship.

    Args:
        spaceship (SpaceshipSchemaReceived): Spaceship data to be added.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        SpaceshipSchemaStored: Newly added spaceship.
    """
    ship = ship_repo.create(
        db=db,
        name=spaceship.name,
        available=True,
        price_per_hour=spaceship.price_per_hour,
        max_speed=spaceship.max_speed,
        max_range=spaceship.max_range
    )
    return ship


@router.get("/", response_model=List[SpaceshipSchemaStored], status_code=200)
async def get_all_spaceships(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number for pagination"),
        limit: int = Query(10, le=10000, description="Number of items per page")
):
    """
    Endpoint to list all spaceships with pagination and offset support.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).
        page (int, optional): Page number for pagination. Defaults to 1.
        limit (int, optional): Number of items per page. Defaults to 10.

    Returns:
        List[SpaceshipSchemaStored]: List of spaceships.
    """
    offset = (page - 1) * limit
    spaceships = ship_repo.fetch_all(db=db, offset=offset, limit=limit)
    if not spaceships:
        raise HTTPException(status_code=404, detail="Spaceships not found")
    return spaceships


@router.get("/{spaceship_id}", response_model=SpaceshipSchemaStored, status_code=200)
async def get(spaceship_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get details of a specific spaceship by ID.

    Args:
        spaceship_id (int): ID of the spaceship.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        SpaceshipSchemaStored: Details of the spaceship.
    """
    ships = ship_repo.fetch_one(db=db, item_id=spaceship_id)
    if not ships:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    return ships


@router.put("/{spaceship_id}", response_model=SpaceshipSchemaStored)
async def update_one_spaceship(spaceship_id: int, spaceship: SpaceshipSchemaReceived, db: Session = Depends(get_db)):
    """
    Endpoint to update details of an existing spaceship.

    Args:
        spaceship_id (int): ID of the spaceship to be updated.
        spaceship (SpaceshipSchemaReceived): Updated spaceship data.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        SpaceshipSchemaStored: Updated spaceship details.
    """
    ships = ship_repo.update_one(db=db, item_id=spaceship_id, **jsonable_encoder(spaceship))
    if not ships:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    return ships


@router.delete("/{spaceship_id}", response_model=SpaceshipSchemaStored)
async def delete_spaceship(spaceship_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a spaceship.

    Args:
        spaceship_id (int): ID of the spaceship to be deleted.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        SpaceshipSchemaStored: Details of the deleted spaceship.
    """
    ship_deleted = ship_repo.delete_one(db, spaceship_id)
    if not ship_deleted:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    return ship_deleted
