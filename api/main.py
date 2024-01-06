from typing import Union
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    print(f"Started on {os.getenv('API_IP')}:{os.getenv('API_PORT')} with Mode {os.getenv('DEBUG')}")
    uvicorn.run("main:app", reload=True, log_level="info")