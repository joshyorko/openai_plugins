from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

class Item(BaseModel):
    name: str
    done: Optional[bool] = False

# Here we changed todos from a list to a dictionary, so we can have todos per user
todos = {}
item_counter = 0

@app.get("/todos/{username}")
async def get_todos(username: str):
    return todos.get(username, [])

@app.post("/todos/{username}")
async def create_item(username: str, item: Item):
    global item_counter
    if username not in todos:
        todos[username] = []
    item_dict = item.dict()
    item_dict["id"] = item_counter
    todos[username].append(item_dict)
    item_counter += 1
    return item_dict

@app.delete("/todos/{username}/{item_id}")
async def delete_item(username: str, item_id: int):
    if username in todos:
        todos[username] = [item for item in todos[username] if item["id"] != item_id]
        return {"message": "Todo deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/.well-known/ai-plugin.json", include_in_schema= False)
async def serve_manifest():
    return FileResponse('ai-plugin.json')
    
@app.get("/openapi.yaml", include_in_schema= False)
async def serve_openapi():
    return FileResponse('openapi.yaml')
    
@app.get("/logo.png", include_in_schema= False)
async def serve_openapi():
    return FileResponse('logo.png')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
