from sqlalchemy import Column, Uuid, String
from database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Uuid(as_uuid=True), primary_key=True, index=True)
    email = Column(String, index=True)
    forename = Column(String, index=True)
    lastname = Column(String, index=True)
    password = Column(String, index=True)
    