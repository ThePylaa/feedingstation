from sqlalchemy import Column, Uuid, String
from utils.db.db import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    forename = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    password_hash = Column(String, index=True, nullable=False)
    