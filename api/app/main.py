from typing import Union
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from models import accepted_animals, animal, feedingstation, portion, user

load_dotenv()

app = FastAPI(

    title="API for the project innovative Feeding Station",
    description="This is the API for the project innovative Feeding Station for the DHBW Heidenheim",
    summary="Created by Max Loehr, Paul Brilmayer",
    docs_url="/",
    version="v0.0.1",

)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    print(f"Started on {os.getenv('API_IP')}:{os.getenv('API_PORT')} with Mode {os.getenv('DEBUG')}")
    uvicorn.run("main:app", reload=True, log_level="info")