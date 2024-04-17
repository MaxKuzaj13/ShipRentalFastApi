import os
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import get_db
from repositories.users import user_repo
from schemas.users import UserSchemaStored, UserSchemaReceived
from schemas.bookings import BookingsSchemaStored
from schemas.ships import SpaceshipSchemaStored

router = APIRouter(
    prefix='/users',
    tags=['users']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# get env from file
SECRET_KEY = os.getenv("SECRET_KEY", "TEST")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def verify_password(plain_password, hashed_password):
    """
    Verify if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password to be compared against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password):
    """
    Hash the provided password.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


class UserInDB(UserSchemaStored):
    """A representation of a user stored in the database."""

    hashed_password: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create an access token.

    Args:
        data (dict): The payload data to be encoded into the token.
        expires_delta (timedelta, optional): The duration of time before the token expires.
            Defaults to None.

    Returns:
        str: The encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db, username: str, password: str):
    """Authenticate a user."""
    user = user_repo.get_user_by_identifier(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


class Token(BaseModel):
    """Token model."""

    access_token: str
    token_type: str


@router.post("/token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
       Get an access token by logging in.

       Authenticates a user with the provided credentials and returns an access token if successful.

       Args:
           db (Session, optional): The database session. Defaults to Depends(get_db).
           form_data (OAuth2PasswordRequestForm, optional): The form data containing the user's credentials. Defaults to Depends().

       Raises:
           HTTPException: If the provided username or password is incorrect.

       Returns:
           Token: An access token.
       """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/", response_model=UserSchemaStored, status_code=201)
async def create_user(user: UserSchemaReceived, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (UserSchemaReceived): User data to be created.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        UserSchemaStored: Newly created user.
    """
    hashed_password = get_password_hashed(user.password)
    new_user = user_repo.create(
        db=db,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        email=user.email,
        active_user=True,
    )
    return new_user


@router.get("/{user_id}/bookings")#, response_model=BookingsSchemaStored)
async def get_bookings(user_id: int, db: Session = Depends(get_db)):
    return user_repo.get_user_bookings(db, user_id)