from sqlalchemy import Column, ForeignKey, Uuid
from utils.db.db import Base

class Accepted_Animals_Model(Base):
    __tablename__ = "accepted_animals"

    accepted_animals_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    feedingstation_id = Column(Uuid(as_uuid=True), ForeignKey("feedingstation.feedingstation_id"), index=True, nullable=False)
    animal_id = Column(Uuid(as_uuid=True), ForeignKey("animal.animal_id"), index=True, nullable=False)
