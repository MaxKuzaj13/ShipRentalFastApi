from fastapi import APIRouter
from fastapi import HTTPException, Path
from typing import Dict

from schemas.ships import Starship

router = APIRouter(prefix='/starships', tags=['starships'])



# Mock Database
starships_db = {
    1: {"name": "Millennium Falcon", "price_per_hour": 1000, "available": True},
    2: {"name": "X-wing", "price_per_hour": 800, "available": True},
    3: {"name": "Star Destroyer", "price_per_hour": 5000, "available": False},
}




@router.get("/", response_model=Dict[int, Starship])
async def list_starships() -> Starship:
    return starships_db

@router.get("/{starship_id}", response_model=Starship)
async def get_starship(starship_id: int = Path(..., title="The ID of the starship to get")):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    return starships_db[starship_id]

@router.post("/", response_model=Starship, status_code=201)
async def create_starship(starship: Starship):
    new_id = max(starships_db.keys()) + 1
    new_starship = Starship(id=new_id, name=starship.name, available=True, price_per_hour=starship.price_per_hour)
    starships_db[new_id] = new_starship.dict()
    return starship

@router.put("/{starship_id}", response_model=Starship)
async def update_starship(starship_id: int, starship: Starship):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    starships_db[starship_id] = starship.dict()
    return starship

@router.delete("/{starship_id}", response_model=None)
async def delete_starship(starship_id: int):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    del starships_db[starship_id]
    return starships_db
