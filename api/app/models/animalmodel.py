from sqlalchemy import Column, ForeignKey, Uuid, String
from utils.db.db import Base

class Animal_Model(Base):
    __tablename__ = "animal"

    animal_rfid = Column(String, primary_key=True, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("user.user_id") ,index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    