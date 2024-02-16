from pydantic import BaseModel
import uuid
from datetime import datetime

class uploadPicture(BaseModel):
    user_id: uuid.UUID
    feedingstation_id: uuid.UUID
    picture: bytes
    creation_date: datetime
