from sqlalchemy import Column, ForeignKey, Uuid, String
from utils.db.db import Base

class Animal(Base):
    __tablename__ = "animal"

    animal_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("user.user_id") ,index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    