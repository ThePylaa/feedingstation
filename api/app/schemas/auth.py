from pydantic import BaseModel
import uuid

class createToken(BaseModel):
    token_id: uuid.UUID
  