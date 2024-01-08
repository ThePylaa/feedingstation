import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response


from utils.db.db import engine, SessionLocal

#Import different Models 
from models import accepted_animalsmodel, animalmodel, feedingstationmodel, portionmodel, usermodel

#Import different Routers 
from routers import user, feedingstation


load_dotenv()

#Generate Table
usermodel.Base.metadata.create_all(bind=engine)
feedingstationmodel.Base.metadata.create_all(bind=engine)

app = FastAPI(

    title="API for the project innovative Feeding Station",
    description="This is the API for the project innovative Feeding Station for the DHBW Heidenheim",
    summary="Created by Max Loehr, Paul Brilmayer",
    docs_url="/",
    version="v0.0.1",

)

#Add Routes to the API
app.include_router(user.router)
app.include_router(feedingstation.router)

#DB Middleware
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

if __name__ == "__main__":
    print(f"Started on {os.getenv('API_IP')}:{os.getenv('API_PORT')} with Mode {os.getenv('DEBUG')}")
    uvicorn.run("main:app", host=os.getenv('API_IP'), port=int(os.getenv('API_PORT')), reload=True, log_level="info")