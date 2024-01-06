from pydantic import BaseModel
import uuid

class FeedingStation(BaseModel):
    feedingstation_id: uuid.UUID
    user_id: uuid.UUID
    name: str
    container_foodlevel: bool