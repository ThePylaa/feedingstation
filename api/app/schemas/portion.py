from pydantic import BaseModel
import datetime
import uuid

class Portion(BaseModel):
    portion_id: uuid.UUID
    accepted_animals_id: uuid.UUID
    time: datetime.datetime
    size : int