from pydantic import BaseModel
import uuid

class User(BaseModel):
    uuid: uuid.UUID
    email: str
    forename: str
    surname: str

class TestMessage(BaseModel):
    message: str
    
