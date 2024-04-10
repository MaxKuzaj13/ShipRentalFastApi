from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db import get_db
from repositories.customers import customers_repo
from schemas.customers import CustomerSchemaReceived, CustomerSchemaStored

router = APIRouter(prefix='/customers', tags=['customers'])


@router.get("/{customers_id}", response_model=CustomerSchemaStored, status_code=200)
async def get_customer(customers_id: int, db: Session = Depends(get_db)):
    customer_data = customers_repo.fetch_one(db=db, item_id=customers_id)
    if not customer_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_data


@router.post("/", response_model=CustomerSchemaStored, status_code=201)
async def create_customer(customer: CustomerSchemaReceived, db: Session = Depends(get_db)):
    new_customer = customers_repo.create(
        db=db,
        name=customer.name,
        document_number=customer.document_number,
        address=customer.address
    )
    return new_customer


@router.get("/", response_model=List[CustomerSchemaStored], status_code=200)
async def list_customers(db: Session = Depends(get_db)):
    customers = customers_repo.fetch_all(db=db)
    if not customers:
        raise HTTPException(status_code=404, detail="Customers not found")
    return customers


@router.put("/{customer_id}", response_model=CustomerSchemaStored)
async def update_customer(customer_id: int, customer: CustomerSchemaReceived, db: Session = Depends(get_db)):
    updated_customer = customers_repo.update_one(db=db, item_id=customer_id, **jsonable_encoder(customer))
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@router.delete("/{customer_id}", response_model=None)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    deleted_customer = customers_repo.delete_one(db=db, item_id=customer_id)
    if not deleted_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
