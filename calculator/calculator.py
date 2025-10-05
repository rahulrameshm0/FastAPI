from fastapi import FastAPI

app = FastAPI()
# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}


@app.get("/users")
async def read_users():
    return ["rick", "john"]
@app.get("/users")
async def read_users2():
    return ["sanu", "manu"]