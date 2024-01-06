from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from sqlalchemy.orm import Session
from models.usermodel import Usermodel
from utils.db.db import get_db
from schemas.users import *
from uuid import uuid4

# This is the user router. It is used to get the information of the current user, to update the information of the current user, to register a new user and to sign in and out.
router = APIRouter(tags=["user"],prefix="/user")

@router.get("/me",response_model=TestMessage)
def info():
    return {"message": "457871ba-125b-4486-b291-9da3afd640fb"}

@router.post("/register")
def register(user: createUser, db: Session = Depends(get_db)):

    existing_email = db.query(Usermodel).filter(Usermodel.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    uuid = uuid4()
    #TODO: Hash password!!!!!
    hashed_password = user.password
    ##########################
    dbUser = Usermodel(user_id=uuid, email=user.email, forename=user.forename, lastname=user.lastname, password_hash=hashed_password)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser

@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
    