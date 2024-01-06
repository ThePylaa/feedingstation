from sqlalchemy import Column, ForeignKey, Uuid, String, Boolean
from database import Base

class FeedingStation(Base):
    __tablename__ = "feedingstation"

    feedingstation_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("user.user_id") ,index=True)
    name = Column(String, index=True)
    container_foodlevel = Column(Boolean, index=True)