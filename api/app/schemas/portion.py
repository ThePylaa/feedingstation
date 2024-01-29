from pydantic import BaseModel
import uuid
from datetime import time

class createPortion(BaseModel):
    time: time
    size: str
    feedingstation_id: uuid.UUID
    animal_rfid: str