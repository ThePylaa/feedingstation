from pydantic import BaseModel
import uuid

class Feedingstation(BaseModel):
    feedingstation_id: uuid.UUID
    user_id: uuid.UUID
    name: str
    container_foodlevel: bool

class createFeedingstation(BaseModel):
    feedingstation_id: uuid.UUID
    name: str

class updateFeedingstation(BaseModel):
    feedingstation_id: uuid.UUID
    container_foodlevel: bool
