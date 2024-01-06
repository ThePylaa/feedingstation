from sqlalchemy import Column, Uuid, String, ForeignKey, DateTime
from utils.db.db import Base

class Portion(Base):
    __tablename__ = "portion"

    portion_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    accepted_animals_id = Column(Uuid(as_uuid=True), ForeignKey("accepted_animals.accepted_animals_id") ,index=True)
    time = Column(DateTime, index=True)
    size = Column(String, index=True)
    