from pydantic import BaseModel
import uuid

class User(BaseModel):
    user_id: uuid.UUID
    email: str
    forename: str
    lastname: str
    password_hash: str

class createUser(BaseModel):
    email: str
    forename: str
    lastname: str
    password: str


class deleteUser(BaseModel):
    user_id: uuid.UUID

class loginUser(BaseModel):
    email: str
    password: str

class TestMessage(BaseModel):
    message: str
    
