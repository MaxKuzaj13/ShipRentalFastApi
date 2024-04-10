from fastapi import APIRouter
from fastapi import HTTPException, Path
from typing import Dict

from schemas.ships import SpaceshipSchemaReceived, SpaceshipSchemaStored

router = APIRouter(prefix='/spaceships', tags=['spaceships'])

# Mock Database
spaceships_db = {
    1: {"name": "Millennium Falcon", "price_per_hour": 1000, "available": True, "max_range": 1000, "max_speed": 1000, "id": 1},
    2: {"name": "X-wing", "price_per_hour": 800, "available": True, "max_range": 800, "max_speed": 200, "id": 2},
    3: {"name": "Star Destroyer", "price_per_hour": 5000, "available": False, "max_range": 100, "max_speed": 1, "id": 3},
}


@router.get("/", response_model=Dict[int, SpaceshipSchemaStored])
async def list_spaceships() -> SpaceshipSchemaStored:
    return spaceships_db


@router.get("/{spaceship_id}", response_model=SpaceshipSchemaStored)
async def get_spaceship(spaceship_id: int = Path(..., title="The ID of the spaceship to get")):
    if spaceship_id not in spaceships_db:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    spaceship_data = spaceships_db[spaceship_id]
    spaceship_data["id"] = spaceship_id
    return spaceship_data


@router.post("/", response_model=SpaceshipSchemaReceived, status_code=201)
async def create_spaceship(spaceship: SpaceshipSchemaReceived):
    new_id = max(spaceships_db.keys()) + 1
    new_spaceship = SpaceshipSchemaStored(
        id=new_id,
        name=spaceship.name,
        available=True,
        price_per_hour=spaceship.price_per_hour,
        max_speed=spaceship.max_speed,
        max_range=spaceship.max_range
    )
    spaceships_db[new_id] = new_spaceship.dict()
    return new_spaceship


@router.put("/{spaceship_id}", response_model=SpaceshipSchemaStored)
async def update_spaceship(spaceship_id: int, spaceship: SpaceshipSchemaReceived):
    if spaceship_id not in spaceships_db:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    updated_spaceship = SpaceshipSchemaStored(
        id=spaceship_id,
        name=spaceship.name,
        price_per_hour=spaceship.price_per_hour,
        available=spaceship.available,
        max_range=spaceship.max_range,
        max_speed=spaceship.max_speed
    )
    spaceships_db[spaceship_id] = updated_spaceship.dict()
    return updated_spaceship


@router.delete("/{spaceship_id}", response_model=None)
async def delete_spaceship(spaceship_id: int):
    if spaceship_id not in spaceships_db:
        raise HTTPException(status_code=404, detail="Spaceship not found")
    del spaceships_db[spaceship_id]
    return spaceships_db