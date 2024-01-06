from sqlalchemy import Column, ForeignKey, Uuid, String, Boolean
from utils.db.db import Base

class FeedingStation_Model(Base):
    __tablename__ = "feedingstation"

    feedingstation_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("user.user_id") ,index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    container_foodlevel = Column(Boolean, index=True, nullable=True)