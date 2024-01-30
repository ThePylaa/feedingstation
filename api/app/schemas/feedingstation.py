from pydantic import BaseModel
import uuid

class Feedingstation(BaseModel):
    feedingstation_id: uuid.UUID
    user_id: uuid.UUID
    name: str
    container_foodlevel: bool
    humidity: str

class createFeedingstation(BaseModel):
    feedingstation_id: uuid.UUID
    name: str

class updateFoodlevel(BaseModel):
    feedingstation_id: uuid.UUID
    container_foodlevel: bool

class updateHumidity(BaseModel):
    feedingstation_id: uuid.UUID
    humidity: str
