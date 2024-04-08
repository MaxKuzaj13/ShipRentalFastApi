from fastapi import APIRouter
from fastapi import HTTPException, Path
from typing import Dict

from schemas.customers import CustomerSchema

router = APIRouter(prefix='/customers', tags=['customers'])

# Mock Database
customers_db = {
    1: {"id": 1, "name": "Max Rogowski", "address": "3ciego maja 19, Warszawa", "document_number": "ABS123456"},
    2: {"id": 2, "name": "Adaś Mialczyński", "address": "1go maja 33, Łódź", "document_number": "ABS123456"},
    3: {"id": 3, "name": "Robert Ixiński", "address": "Piotrkowska 120, Łódź", "document_number": "ABS123456"},
}


@router.get("/", response_model=Dict[int, CustomerSchema])
async def list_customer() -> CustomerSchema:
    return customers_db


@router.get("/{customers_id}", response_model=CustomerSchema)
async def get_customer(customers_id: int = Path(..., title="The ID of the customer to get")):
    if customers_id not in customers_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    customer_data = customers_db[customers_id]
    customer_data["id"] = customers_id
    return customer_data


@router.post("/", response_model=CustomerSchema, status_code=201)
async def create_customer(customer: CustomerSchema):
    new_id = max(customers_db.keys()) + 1
    new_customer = CustomerSchema(
        id=new_id,
        name=customer.name,
        document_number=customer.document_number,
        address=customer.address
    )
    customers_db[new_id] = new_customer.dict()
    return new_customer


@router.put("/{customers_id}", response_model=CustomerSchema)
async def update_customer(customers_id: int, customer: CustomerSchema):
    if customers_id not in customers_db:
        raise HTTPException(status_code=404, detail="Starship not found")
    updated_customers = CustomerSchema(
        id=customers_id,
        name=customer.name,
        address=customer.address,
        document_number=customer.document_number
    )
    customers_db[customers_id] = updated_customers.dict()
    return updated_customers


@router.delete("/{customers_id}", response_model=None)
async def delete_customer(customers_id: int):
    if customers_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    del customers_db[customers_id]
    return customers_db
