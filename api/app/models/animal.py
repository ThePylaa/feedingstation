from sqlalchemy import Column, ForeignKey, Uuid, String
from utils.db.db import Base

class Animal(Base):
    __tablename__ = "animal"

    animal_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("user.user_id") ,index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    