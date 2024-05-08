from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from database import db_dependency
from pydantic_models import CreateUserRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])

SECRETKEY_KEY = "7bc621fbc40de68f79b84a3922992194655724e9df7e2b8d684e01073395104f"
ALGORITHM = "HS256"

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(db: db_dependency, create_user_request: CreateUserRequest):
    print("kucreate user", create_user_request)
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bycrypt_context.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created successfully"}

    


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        print("user kwa authenticate", user)
        return False
    if not bycrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id:int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRETKEY_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=Token)
async def login(
    form_data:Annotated[OAuth2PasswordRequestForm, Depends()] , db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        print("akilogin pale kwa error", user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

async def get_active_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRETKEY_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        else:
            return {'username': username, "id": user_id}
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")



