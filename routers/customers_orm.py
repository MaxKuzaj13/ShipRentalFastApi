from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db import get_db
from repositories.customers import customers_repo
from schemas.customers import CustomerSchemaReceived, CustomerSchemaStored

router = APIRouter(prefix='/customers', tags=['customers'])


@router.post("/", response_model=CustomerSchemaStored, status_code=201)
async def create_customer(customer: CustomerSchemaReceived, db: Session = Depends(get_db)):
    """
    Endpoint to create a new customer.

    Args:
        customer (CustomerSchemaReceived): Customer data to be created.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        CustomerSchemaStored: Newly created customer.
    """
    new_customer = customers_repo.create(
        db=db,
        name=customer.name,
        document_number=customer.document_number,
        address=customer.address
    )
    return new_customer


@router.get("/", response_model=List[CustomerSchemaStored], status_code=200)
async def list_customers(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number for pagination"),
        limit: int = Query(10, le=10000, description="Number of items per page")
):
    """
    Endpoint to list all customers with pagination and offset support.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).
        page (int, optional): Page number for pagination. Defaults to 1.
        limit (int, optional): Number of items per page. Defaults to 10.

    Returns:
        List[CustomerSchemaStored]: List of customers.
    """
    offset = (page - 1) * limit
    customers = customers_repo.fetch_all(db=db, offset=offset, limit=limit)
    if not customers:
        raise HTTPException(status_code=404, detail="Customers not found")
    return customers


@router.get("/{customer_id}", response_model=CustomerSchemaStored, status_code=200)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get details of a specific customer by ID.

    Args:
        customer_id (int): ID of the customer.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        CustomerSchemaStored: Details of the customer.
    """
    customer_data = customers_repo.fetch_one(db=db, item_id=customer_id)
    if not customer_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_data


@router.put("/{customer_id}", response_model=CustomerSchemaStored)
async def update_customer(customer_id: int, customer: CustomerSchemaReceived, db: Session = Depends(get_db)):
    """
    Endpoint to update details of an existing customer.

    Args:
        customer_id (int): ID of the customer to be updated.
        customer (CustomerSchemaReceived): Updated customer data.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        CustomerSchemaStored: Updated customer details.
    """
    updated_customer = customers_repo.update_one(db=db, item_id=customer_id, **jsonable_encoder(customer))
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@router.delete("/{customer_id}", response_model=None)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a customer.

    Args:
        customer_id (int): ID of the customer to be deleted.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        None
    """
    deleted_customer = customers_repo.delete_one(db=db, item_id=customer_id)
    if not deleted_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
