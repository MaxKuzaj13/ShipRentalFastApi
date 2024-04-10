from fastapi import FastAPI, Request, APIRouter, Response
from routers import ships_orm, customers_orm, bookings_orm, attachments

from db import engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


# Include routers from ships, customers, bookings
app.include_router(ships_orm.router)
app.include_router(customers_orm.router)
app.include_router(bookings_orm.router)
app.include_router(attachments.router)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
       Middleware function to manage database sessions.

       This middleware function creates a new database session for each incoming request
       and attaches it to the request object. After processing the request, it closes the session.

       Args:
           request (Request): The incoming HTTP request.
           call_next (Callable): The next function in the request-response cycle.

       Returns:
           Response: The HTTP response.
       """
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    # except Exception as e:
    #     response = Response(f"Not implemented: {e}", status_code=501)
    finally:
        request.state.db.close()
    return response
