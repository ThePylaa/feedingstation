from sqlalchemy import Column, Uuid, String, ForeignKey, DateTime
from utils.db.db import Base

class Portion(Base):
    __tablename__ = "portion"

    portion_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    accepted_animals_id = Column(Uuid(as_uuid=True), ForeignKey("accepted_animals.accepted_animals_id") ,index=True, nullable=False)
    time = Column(DateTime, index=True, nullable=False)
    size = Column(String, index=True, nullable=False)
    