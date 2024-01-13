from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.usermodel import User_Model
from models.user_tokenmodel import User_Token_Model
from utils.db.db import get_db
from utils.auth.auth import hashPassword, verify_password, create_access_token, decode_access_token
from schemas.users import *
from datetime import datetime, timedelta
from uuid import uuid4


# This is the user router. It is used to get the information of the current user, to update the information of the current user, to register a new user and to sign in and out.
router = APIRouter(tags=["user"],prefix="/user")

@router.get("/me",response_model=User)
def info():
    decode = decode_access_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiN2FiOTU0Y2ItMGJiOC00YzdhLTllMDAtZTlmYWRjZTk0MTI4IiwiZXhwIjoxNzA1MTY0MTEyfQ.bFwjkD0SeaW84CJ05vyrH_i0HhBe89ot9RrwmYo4OiU")
    print(decode)
    print(datetime.utcnow() + timedelta(minutes=30))
    return {
        "user_id": uuid4(),
        "email": "Hans",
        "forename": "Hans",
        "lastname": "Hans",
        "password_hash": "Hans"
    }


@router.post("/register")
def register(user: createUser, db: Session = Depends(get_db)):
    """Function to register a new user. The user has to provide an email, a forename, a lastname and a password. The password is hashed before it is stored in the database. Email has to be unique."""
    existing_email = db.query(User_Model).filter(User_Model.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=406, detail="Email already registered")
    
    uuid = uuid4()
    hashed_password = hashPassword(user.password)
    dbUser = User_Model(user_id=uuid, email=user.email, forename=user.forename, lastname=user.lastname, password_hash=hashed_password)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser
    
@router.post("/login")
def login(form_data: loginUser = Depends(),db: Session = Depends(get_db)):
    """Function to get a standard oauth2 token"""
    email = form_data.email
    password = form_data.password

    db_user = db.query(User_Model).filter(User_Model.email == email).first()
    if db_user:
        if verify_password(password,db_user.password_hash):
            token_data = {
                "user_id":str(db_user.user_id),
            }
            token = create_access_token(token_data)
            dbtoken = User_Token_Model(token=token, user_id = db_user.user_id, creation_date = datetime.now()) 
            db.add(dbtoken)
            db.commit()
            db.refresh(dbtoken)
            content = {"access_token": token, "token_type": "bearer"}
            response = JSONResponse(content=content)
            response.set_cookie(key="access_token", value=token)
            return token 
        else:
            raise HTTPException(
            status_code=401,
            detail="Incorrect Password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect Username",
            headers={"WWW-Authenticate": "Bearer"},
        )
@router.delete("/delete")
def delete(user: deleteUser, db: Session = Depends(get_db)):
    """Function to delete a user. The user can be identified by the uuid or the email"""
    try:
        uuid.UUID(user.info)
        db_user = db.query(User_Model).filter(User_Model.uuid == user.info).first()
    except:
        db_user = db.query(User_Model).filter(User_Model.email == user.info).first()

    if db_user != None:
        db.delete(db_user)
        db.commit()
        return db_user
    raise HTTPException(
        status_code=400,
        detail="No User Found"
    )

@router.get("/get_all_user")
def get_all_users(db: Session = Depends(get_db)):
    """Function that returns all users"""
    return db.query(User_Model).all()