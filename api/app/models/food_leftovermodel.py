from sqlalchemy import Column, String, ForeignKey, Float, DateTime, Uuid
from utils.db.db import Base

class Food_Leftover_Model(Base):
    __tablename__ = "food_leftover"

    food_leftover_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    animal_rfid = Column(String, ForeignKey("animal.animal_rfid"), nullable=False)
    weight = Column(Float, index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)