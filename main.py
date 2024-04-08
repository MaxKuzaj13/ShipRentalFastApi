from fastapi import FastAPI
from routers import ships, customers


app = FastAPI()

# Include routers from ships
app.include_router(ships.router)
app.include_router(customers.router)
