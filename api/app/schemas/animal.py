from pydantic import BaseModel
import uuid
import datetime

class createAnimal(BaseModel):
    animal_rfid: str
    user_id: uuid.UUID
    name: str
    type: str

class postFoodLeftover(BaseModel):
    animal_rfid: str
    weight: float
    date: datetime.datetime
