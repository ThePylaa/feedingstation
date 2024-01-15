from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.db.db import get_db
from utils.auth.auth import hashPassword, verify_password, create_access_token
from schemas.feedingstation import *
from models.feedingstationmodel import FeedingStation_Model
from datetime import datetime
from uuid import uuid4


# This is the user router. It is used to get the information of the current user, to update the information of the current user, to register a new user and to sign in and out.
router = APIRouter(tags=["feedingstation"],prefix="/feedingstation")

@router.get("/all_stations")
def get_all_stations(db: Session = Depends(get_db)):
    """Function that returns all feeediong stations"""
    stations = db.query(FeedingStation_Model).all()
    if not stations:
        raise HTTPException(status_code=404, detail="No feedingstations found, db empty")
    return stations

@router.post("/register")
def register(feedingstation: createFeedingstation, db: Session = Depends(get_db)):

    existing_station = db.query(FeedingStation_Model).filter(FeedingStation_Model.feedingstation_id == feedingstation.feedingstation_id).first()
    if existing_station:
        raise HTTPException(status_code=406, detail="Feedingstation already registered")
    
    dbStation = FeedingStation_Model(feedingstation_id=feedingstation.feedingstation_id, name=feedingstation.name)
    db.add(dbStation)
    db.commit()
    db.refresh(dbStation)
    return dbStation