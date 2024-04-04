from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Mock Database
starships_db = {
    1: {"name": "Millennium Falcon", "price_per_hour": 1000, "available": True},
    2: {"name": "X-wing", "price_per_hour": 800, "available": True},
    3: {"name": "Star Destroyer", "price_per_hour": 5000, "available": False},
}

class Starship(BaseModel):
    name: str
    price_per_hour: float
    available: bool

class StarshipCreate(BaseModel):
    name: str
    price_per_hour: float

@app.get("/starships/", response_model=Dict[int, Starship])
async def list_starships():
    return starships_db

@app.get("/starships/{starship_id}", response_model=Starship)
async def get_starship(starship_id: int = Path(..., title="The ID of the starship to get")):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    return starships_db[starship_id]

@app.post("/starships/", response_model=Starship)
async def create_starship(starship: StarshipCreate):
    new_id = max(starships_db.keys()) + 1
    starships_db[new_id] = starship.dict()
    return starship

@app.put("/starships/{starship_id}", response_model=Starship)
async def update_starship(starship_id: int, starship: StarshipCreate):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    starships_db[starship_id] = starship.dict()
    return starship

@app.delete("/starships/{starship_id}", response_model=None)
async def delete_starship(starship_id: int):
    if starship_id not in starships_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    del starships_db[starship_id]
    return None
