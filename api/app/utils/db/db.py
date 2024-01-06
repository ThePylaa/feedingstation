import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fastapi import Request

load_dotenv()

#Database Connection
SQLALCHEMYPost_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_IP')}/{os.getenv('DB_NAME')}"

engine = create_engine(SQLALCHEMYPost_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
connection = engine.connect()

# Dependency
def get_db(request: Request):
    return request.state.db