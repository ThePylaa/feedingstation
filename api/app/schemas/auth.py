from pydantic import BaseModel
import uuid

class createToken(BaseModel):
    uuid: uuid.UUID
  