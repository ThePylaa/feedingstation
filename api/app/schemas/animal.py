from pydantic import BaseModel
import uuid

class createAnimal(BaseModel):
    animal_rfid: str
    user_id: uuid.UUID
    name: str
    type: str