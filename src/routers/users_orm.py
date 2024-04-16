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

router = APIRouter(
    prefix='/users',
    tags=['users']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
# TODO Move to env
SECRET_KEY = "620191445bbb51e8f590a53cb80b8a9b8a818fe6f5be22c3b9d5a3c078078b3e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password):
    return pwd_context.hash(password)


class UserInDB(UserSchemaStored):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db, username: str, password: str):
    user = user_repo.get_user_by_identifier(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/", response_model=UserSchemaStored, status_code=201)
async def create_user(user: UserSchemaReceived, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user.

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
