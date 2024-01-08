from sqlalchemy import Column, Uuid, String, ForeignKey, TIMESTAMP
from utils.db.db import Base

class User_Token_Model(Base):
    __tablename__ = "user_token"

    token = Column(String, primary_key=True, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("user.user_id") ,index=True, nullable=False)
    creation_date = Column(TIMESTAMP, index=True, nullable=False)
    