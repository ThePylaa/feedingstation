from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.db.db import get_db
from schemas.picture_log import *
from models.picture_logmodel import Picture_Log_Model
from uuid import uuid4
from datetime import datetime, timedelta


router = APIRouter(tags=["picture"],prefix="/picture")

@router.get("/all_pictures_by_userid")
def get_all_pictures_by_userid(user_id: str, db: Session = Depends(get_db)):
    """Function that returns all pictures of a user"""
    delete_expired_pictures(db)
    
    pictures = db.query(Picture_Log_Model).filter(Picture_Log_Model.user_id == user_id).all()
    if not pictures:
        raise HTTPException(status_code=404, detail="No pictures found")
    return pictures

@router.get("/last_picture_by_userid")
def get_last_picture_by_userid(user_id: str, db: Session = Depends(get_db)):
    """Function that returns the last picture of a user"""
    delete_expired_pictures(db)

    picture = db.query(Picture_Log_Model).filter(Picture_Log_Model.user_id == user_id).order_by(Picture_Log_Model.creation_date.desc()).first()
    if not picture:
        raise HTTPException(status_code=404, detail="No pictures found")
    return picture

@router.get("/all_pictures_by_feedingstationid")
def get_all_pictures_by_feedingstationid(feedingstation_id: str, db: Session = Depends(get_db)):
    """Function that returns all pictures of a feedingstation"""
    delete_expired_pictures(db)

    pictures = db.query(Picture_Log_Model).filter(Picture_Log_Model.feedingstation_id == feedingstation_id).all()
    if not pictures:
        raise HTTPException(status_code=404, detail="No pictures found")
    return pictures

@router.get("/last_picture_by_feedingstationid")
def get_last_picture_by_feedingstationid(feedingstation_id: str, db: Session = Depends(get_db)):
    """Function that returns the last picture of a feedingstation"""
    delete_expired_pictures(db)

    picture = db.query(Picture_Log_Model).filter(Picture_Log_Model.feedingstation_id == feedingstation_id).order_by(Picture_Log_Model.creation_date.desc()).first()
    if not picture:
        raise HTTPException(status_code=404, detail="No pictures found")
    return picture

@router.post("/upload_picture")
def upload_picture(picture: uploadPicture, db: Session = Depends(get_db)):
    '''Function to upload a picture. The user has to provide the picture_id, the user_id, the feedingstation_id, the picture and the creation_date. The picture is stored in the database'''
    delete_expired_pictures(db)

    picture_id = uuid4()
    while db.query(Picture_Log_Model).filter(Picture_Log_Model.picture_id == picture_id).first():
        picture_id = uuid4()

    dbPicture = Picture_Log_Model(picture_id=picture_id, user_id=picture.user_id, feedingstation_id=picture.feedingstation_id, picture=picture.picture, creation_date=picture.creation_date)
    db.add(dbPicture)
    db.commit()
    db.refresh(dbPicture)
    return dbPicture

@router.delete("/delete_expired_pictures")
def delete_expired_pictures(db: Session = Depends(get_db)):
    """Function to delete pictures that are older than 24 hours"""
    db.query(Picture_Log_Model).filter(Picture_Log_Model.creation_date < datetime.now() - timedelta(days=1)).delete()
    db.commit()
    return "Expired pictures deleted"
    