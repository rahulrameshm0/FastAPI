from email.policy import HTTP
from fastapi import HTTPException, Request, Response
from random import randint
from fastapi import FastAPI
from datetime import datetime
app = FastAPI(root_path="/api/v1")
from typing import Any

data: Any = [
    {"campaign_id": 1,
     "name": "Summer Launch",
     "due_date": datetime.now(),
     "created_at": datetime.now()
     },

    {"campaign_id": 2,
     "name": "Winter Launch",
     "due_date": datetime.now(),
     "created_at": datetime.now()
     }
]

@app.get("/")
async def root():
    return {"Message": "Hello World"}

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaign/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"campaign": campaign}

    raise HTTPException(status_code=404)

@app.post("/campaign", status_code=201)
async def create_campaign(body: dict[str, Any]):
    new: Any = {
        "campaign_id": randint(100,1000),
         "name": body.get("name"),
         "due_date": body.get("due_date"),
         "created_at": datetime.now()
         }

    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{id}")
async def updated_campaign(id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            updated: Any = {
                "campaign_id": randint(100, 1000),
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("Created_at")
            }
            data[index] = updated
            return {"campaign": updated}
    raise HTTPException(status_code=404)

@app.delete("/campaign")
async def delete_campaign(id:int):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404)


