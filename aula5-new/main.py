from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI(
    title="Recipe API",
    description="An API to manage recipes",
    version="1.0.0"
)

items = []

class Item(BaseModel):
    name: str
    description: str = None
    price: float=  None
    quantity: int = None

users = {
    "user1": "password1"
}

security = HTTPBasic()

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = users.get(credentials.username)
    if not correct_password or correct_password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/hello")
async def hello(username: str = Depends(verify_password)):
    return {"message": f"Hello, {username}!"}

@app.get("/items")
async def read_items():
    return items

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    items.append(item)
    return {"message": f"Item successfully created: {item}"}

@app.put("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"message": f"Item successfully updated: {item}"}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    removed = items.pop(item_id)
    return {"message": f"Item successfully removed: {removed}"}

@app.get("/")
async def home():
    return {"message": "Hello, FastAPI!"}