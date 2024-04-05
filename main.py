from fastapi import FastAPI
from routers import ships

app = FastAPI()

# Include routers from ships
app.include_router(ships.router)
