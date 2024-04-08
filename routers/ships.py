from fastapi import APIRouter
from fastapi import HTTPException, Path
from typing import Dict

from schemas.ships import StarshipSchemaReceived, StarshipSchemaStored

router = APIRouter(prefix='/starships', tags=['starships'])

# Mock Database
starships_db = {
    1: {"name": "Millennium Falcon", "price_per_hour": 1000, "available": True, "max_range": 1000, "max_speed": 1000, "id": 1},
    2: {"name": "X-wing", "price_per_hour": 800, "available": True, "max_range": 800, "max_speed": 200, "id": 2},
    3: {"name": "Star Destroyer", "price_per_hour": 5000, "available": False, "max_range": 100, "max_speed": 1, "id": 3},
}


@router.get("/", response_model=Dict[int, StarshipSchemaStored])
async def list_starships() -> StarshipSchemaStored:
    return starships_db


@router.get("/{starship_id}", response_model=StarshipSchemaStored)
async def get_starship(starship_id: int = Path(..., title="The ID of the starship to get")):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    starship_data = starships_db[starship_id]
    starship_data["id"] = starship_id
    return starship_data


@router.post("/", response_model=StarshipSchemaReceived, status_code=201)
async def create_starship(starship: StarshipSchemaReceived):
    new_id = max(starships_db.keys()) + 1
    new_starship = StarshipSchemaStored(
        id=new_id,
        name=starship.name,
        available=True,
        price_per_hour=starship.price_per_hour,
        max_speed=starship.max_speed,
        max_range=starship.max_range
    )
    starships_db[new_id] = new_starship.dict()
    return new_starship


@router.put("/{starship_id}", response_model=StarshipSchemaStored)
async def update_starship(starship_id: int, starship: StarshipSchemaReceived):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    updated_starship = StarshipSchemaStored(
        id=starship_id,
        name=starship.name,
        price_per_hour=starship.price_per_hour,
        available=starship.available,
        max_range=starship.max_range,
        max_speed=starship.max_speed
    )
    starships_db[starship_id] = updated_starship.dict()
    return updated_starship


@router.delete("/{starship_id}", response_model=None)
async def delete_starship(starship_id: int):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    del starships_db[starship_id]
    return starships_db
