from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db import get_db
from repositories.bookings import booking_repo
from repositories.users import user_repo
from schemas.bookings import BookingsSchemaReceived, BookingsSchemaStored

router = APIRouter(prefix='/bookings', tags=['bookings'])


@router.post("/", response_model=BookingsSchemaStored, status_code=201)
async def create_bookings(bookings: BookingsSchemaReceived, db: Session = Depends(get_db)):
    """
    Endpoint to create a new booking.

    Args:
        bookings (BookingsSchemaReceived): Booking data to be created.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        BookingsSchemaStored: Newly created booking.
    """
    new_booking = booking_repo.create(
        db=db,
        ship_id=bookings.ship_id,
        user_id=bookings.user_id,
        date_start=bookings.date_start,
        date_end=bookings.date_end,
    )
    return new_booking


@router.get("/", response_model=List[BookingsSchemaStored], status_code=200)
async def get_all_bookings(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number for pagination"),
        limit: int = Query(10, le=10000, description="Number of items per page")
):
    """
    Endpoint to list all bookings with pagination and offset support.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).
        page (int, optional): Page number for pagination. Defaults to 1.
        limit (int, optional): Number of items per page. Defaults to 10.

    Returns:
        List[BookingsSchemaStored]: List of bookings.
    """
    offset = (page - 1) * limit
    bookings = booking_repo.fetch_all(db=db, offset=offset, limit=limit)
    if not bookings:
        raise HTTPException(status_code=404, detail="Bookings not found")
    return bookings


@router.get("/{booking_id}", response_model=BookingsSchemaStored, status_code=200)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get details of a specific booking by ID.

    Args:
        booking_id (int): ID of the booking.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        BookingsSchemaStored: Details of the booking.
    """
    booking = booking_repo.fetch_one(db=db, item_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=BookingsSchemaStored)
async def update_one_booking(booking_id: int, bookings: BookingsSchemaReceived, db: Session = Depends(get_db)):
    """
    Endpoint to update details of an existing booking.

    Args:
        booking_id (int): ID of the booking to be updated.
        bookings (BookingsSchemaReceived): Updated booking data.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        BookingsSchemaStored: Updated booking details.
    """
    updated_booking = booking_repo.update_one(db=db, item_id=booking_id, **jsonable_encoder(bookings))
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking


@router.delete("/{booking_id}", response_model=BookingsSchemaStored)
async def delete_bookings(booking_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a booking.

    Args:
        booking_id (int): ID of the booking to be deleted.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        BookingsSchemaStored: Deleted booking details.
    """
    booking_deleted = booking_repo.delete_one(db, booking_id)
    if not booking_deleted:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking_deleted


@router.post("/{user_id}/user", response_model=BookingsSchemaStored, status_code=201)
async def add_bookings_by_user(bookings: BookingsSchemaReceived, user_id: int, db: Session = Depends(get_db)):
    user = user_repo.fetch_one(db, user_id)
    booking = user_repo.create_booking_by_user(db, user, bookings)
    return booking
