from sqlalchemy import Column, String, ForeignKey, LargeBinary, DateTime, Uuid
from utils.db.db import Base

class Picture_Log_Model(Base):
    __tablename__ = "picture_log"

    picture_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    feedingstation_id = Column(Uuid(as_uuid=True), ForeignKey("feedingstation.feedingstation_id"), nullable=False)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    picture = Column(LargeBinary, nullable=False)
    creation_date = Column(DateTime, index=True, nullable=False)