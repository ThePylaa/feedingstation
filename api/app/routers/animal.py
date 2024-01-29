from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.db.db import get_db
from models.animalmodel import Animal_Model
from models.usermodel import User_Model
from models.food_leftovermodel import Food_Leftover_Model
from schemas.animal import *
from uuid import uuid4


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

@router.post("/food_leftover")
def post_food_leftover(food_leftover: postFoodLeftover, db: Session = Depends(get_db)):
    '''Function to post the food leftover of an animal'''
    # check if animal_rfid is registered
    existing_animal = db.query(Animal_Model).filter(Animal_Model.animal_rfid == food_leftover.animal_rfid).first()
    if not existing_animal:
        raise HTTPException(status_code=404, detail="Animal not registered")
    
    uuid = uuid4()
    #check if uuid is already in use
    while db.query(Food_Leftover_Model).filter(Food_Leftover_Model.food_leftover_id == uuid).first():
        uuid = uuid4()
    
    dbFood_leftover = Food_Leftover_Model(food_leftover_id=uuid, animal_rfid=food_leftover.animal_rfid, weight=food_leftover.weight, date=food_leftover.date)
    
    db.add(dbFood_leftover)
    db.commit()
    db.refresh(dbFood_leftover)
    return dbFood_leftover

@router.get("/food_leftover")
def get_food_leftover(animal_rfid: str, db: Session = Depends(get_db)):
    '''Function to get all food leftovers of an animal with their timestamps'''
    # check if animal_rfid is registered
    existing_animal = db.query(Animal_Model).filter(Animal_Model.animal_rfid == animal_rfid).first()
    if not existing_animal:
        raise HTTPException(status_code=404, detail="Animal not registered")
    
    return db.query(Food_Leftover_Model).filter(Food_Leftover_Model.animal_rfid == animal_rfid).all()
  