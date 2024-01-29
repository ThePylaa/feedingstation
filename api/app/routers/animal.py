from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.db.db import get_db
from models.animalmodel import Animal_Model
from models.usermodel import User_Model
from schemas.animal import *


router = APIRouter(tags=["animal"],prefix="/animal")

@router.get("/all")
def get_all_animals(db: Session = Depends(get_db)):
    """Function that returns all animals"""
    animals = db.query(Animal_Model).all()
    if not animals:
        raise HTTPException(status_code=404, detail="No animals found, db empty")
    return animals

@router.post("/register")
def register(animal: createAnimal, db: Session = Depends(get_db)):
    '''Function to register a new animal. The user has to provide the animal_rfid, the user_id, the name and the type. The animal_rfid is stored in the database'''

    # check if animal_rfid is already registered
    existing_animal = db.query(Animal_Model).filter(Animal_Model.animal_rfid == animal.animal_rfid).first()
    if existing_animal:
        raise HTTPException(status_code=406, detail="Animal / RFID already registered")
    
    # check if user_id is registered
    existing_user = db.query(User_Model).filter(User_Model.user_id == animal.user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not existing")
    

    dbAnimal = Animal_Model(animal_rfid=animal.animal_rfid, user_id=animal.user_id, name=animal.name, type=animal.type)
    db.add(dbAnimal)
    db.commit()
    db.refresh(dbAnimal)
    return dbAnimal