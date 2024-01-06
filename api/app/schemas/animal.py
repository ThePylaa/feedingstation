from pydantic import BaseModel
import uuid

class Animal(BaseModel):
    animal_id: uuid.UUID
    user_id: uuid.UUID
    name: str
    type: str
