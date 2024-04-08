from fastapi import APIRouter
from fastapi import HTTPException, Path
from typing import Dict

from schemas.bookings import BookingsSchema

router = APIRouter(prefix='/bookings', tags=['bookings'])

# Mock Database
bookings_db = {
    1: {"id": 1, "spaceship_id": 1, "customer_id": 1, "date_start": "2024-04-08 10:00:00", "date_end": "2024-04-09 10:00:00"},
    2: {"id": 2, "spaceship_id": 1, "customer_id": 1, "date_start": "2023-04-08 10:00:00", "date_end": "2023-04-09 10:00:00"},
    3: {"id": 3, "spaceship_id": 1, "customer_id": 1, "date_start": "2022-04-08 10:00:00", "date_end": "2022-04-09 10:00:00"},
}


@router.get("/", response_model=Dict[int, BookingsSchema])
async def list_bookings() -> BookingsSchema:
    return bookings_db


@router.get("/{bookings_id}", response_model=BookingsSchema)
async def get_bookings(bookings_id: int = Path(..., title="The ID of the bookings to get")):
    if bookings_id not in bookings_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    customer_data = bookings_db[bookings_id]
    customer_data["id"] = bookings_id
    return customer_data


@router.post("/", response_model=BookingsSchema, status_code=201)
async def create_bookings(bookings: BookingsSchema):
    new_id = max(bookings_db.keys()) + 1
    new_bookings = BookingsSchema(
        id=new_id,
        spaceship_id=bookings.spaceship_id,
        customer_id=bookings.customer_id,
        date_start=bookings.date_start,
        date_end=bookings.date_end)
    bookings_db[new_id] = new_bookings.dict()
    return new_bookings


@router.put("/{bookings_id}", response_model=BookingsSchema)
async def update_bookings(bookings_id: int, bookings: BookingsSchema):
    if bookings_id not in bookings_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    updated_bookings = BookingsSchema(
        id=bookings_id,
        spaceship_id=bookings.spaceship_id,
        customer_id=bookings.customer_id,
        date_start=bookings.date_start,
        date_end=bookings.date_end)
    bookings_db[bookings_id] = updated_bookings.dict()
    return updated_bookings


@router.delete("/{bookings_id}", response_model=None)
async def delete_bookings(bookings_id: int):
    if bookings_id not in bookings_db:
        raise HTTPException(status_code=404, detail="Bookings not found")
    del bookings_db[bookings_id]
    return bookings_db
