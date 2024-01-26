from sqlalchemy import Column, Uuid, String, ForeignKey, Time
from utils.db.db import Base

class Portion_Model(Base):
    __tablename__ = "portion"

    portion_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    time = Column(Time, index=True, nullable=False)
    size = Column(String, index=True, nullable=False)
    feedingstation_id = Column(Uuid(as_uuid=True), ForeignKey("feedingstation.feedingstation_id"), nullable=False)
    animal_rfid_id = Column(String, ForeignKey("animal.animal_rfid_id"), nullable=False)
    