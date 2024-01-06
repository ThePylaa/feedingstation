from pydantic import BaseModel
import uuid

class Accepted_Animals(BaseModel):
    accepted_animals_id: uuid.UUID
    feedingstation_id: uuid.UUID
    animal_id: uuid.UUID
