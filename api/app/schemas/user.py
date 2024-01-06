from pydantic import BaseModel
import uuid

class User(BaseModel):
    user_id: uuid.UUID
    email: str
    forename: str
    lastname: str
    password: str
    