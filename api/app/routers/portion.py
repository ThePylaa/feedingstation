from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.db.db import get_db
import uuid
from models.portionmodel import Portion_Model
from schemas.portion import *
from models.animalmodel import Animal_Model
from models.feedingstationmodel import FeedingStation_Model


router = APIRouter(tags=["portion"],prefix="/portion")

@router.get("/portions")
def get_portion(feedingstation: uuid.UUID, db: Session = Depends(get_db)):
    """Function that returns all portions when given the uuid of the feedingstation"""
    return db.query(Portion_Model).filter(Portion_Model.feedingstation_id == feedingstation).all()

@router.post("/create_portion")
def create_portion(portion: createPortion, db: Session = Depends(get_db)):
    """Function that adds a portion to the database"""
    portion_id = uuid.uuid4()
    #check if portion_id is already in use
    while db.query(Portion_Model).filter(Portion_Model.portion_id == portion_id).first():
        portion_id = uuid.uuid4()

    #check if animal_rfid_id is registered
    if not db.query(Animal_Model).filter(Animal_Model.animal_rfid_id == portion.animal_rfid_id).first():
        raise HTTPException(status_code=404, detail="Animal not registered")
    
    #check if feedingstation_id is registered
    if not db.query(FeedingStation_Model).filter(FeedingStation_Model.feedingstation_id == portion.feedingstation_id).first():
        raise HTTPException(status_code=404, detail="Feedingstation not registered")
    
    dbPortion = Portion_Model(portion_id=portion_id, time=portion.time, size=portion.size, feedingstation_id=portion.feedingstation_id, animal_rfid_id=portion.animal_rfid_id)
    db.add(dbPortion)
    db.commit()
    db.refresh(dbPortion)
    return dbPortion
