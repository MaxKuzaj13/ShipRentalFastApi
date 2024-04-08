from fastapi import FastAPI
from routers import ships, customers, bookings


app = FastAPI()

# Include routers from ships, customers, bookings
app.include_router(ships.router)
app.include_router(customers.router)
app.include_router(bookings.router)
