from fastapi import APIRouter
from schemas.users import *

# This is the user router. It is used to get the information of the current user, to update the information of the current user, to register a new user and to sign in and out.
router = APIRouter(tags=["user"],prefix="/user")

@router.get("/me",response_model=TestMessage)
def info():
    return {"message": "457871ba-125b-4486-b291-9da3afd640fb"}