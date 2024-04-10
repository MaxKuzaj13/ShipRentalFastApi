from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from repositories.ships import create
from schemas.ships import SpaceshipSchemaReceived

router = APIRouter(prefix='/spaceships', tags=['spaceships'])

# TODO add after table ships will be available on PGSQL
# @router.get("/{spaceship_id}", response_model=SpaceshipSchemaStored)
# async def get_spaceship(spaceship_id: int = Path(..., title="The ID of the spaceship to get")):
#     if spaceship_id not in spaceships_db:
#         raise HTTPException(status_code=404, detail="Spaceship not found")
#     spaceship_data = spaceships_db[spaceship_id]
#     spaceship_data["id"] = spaceship_id
#     return spaceship_data


@router.post("/", response_model=SpaceshipSchemaReceived, status_code=201)
async def add(spaceship: SpaceshipSchemaReceived, db:Session = Depends(get_db)) -> [SpaceshipSchemaReceived]:
    create(
        db=db,
        name=spaceship.name,
        available=True,
        price_per_hour=spaceship.price_per_hour,
        max_speed=spaceship.max_speed,
        max_range=spaceship.max_range
    )
    return spaceship
