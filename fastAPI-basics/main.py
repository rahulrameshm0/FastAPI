from contextlib import asynccontextmanager
from email.policy import HTTP
from fastapi import HTTPException, Request, Response, Depends
from random import randint
from fastapi import FastAPI
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import create_engine, select
from sqlalchemy.orm import session
from typing import Annotated
from sqlmodel import Session, SQLModel, Field



# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# connect_args = {"check_same_thread":False}
# engine = create_engine(sqlite_url,connect_args=connect_args)
# class Campaign(SQLModel, table=True):
#     campaign_id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     due_date: datetime | None = Field(default=None, index=True)
#     creates_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)
# def create_db_and_models():
#     SQLModel.metadata.create_all(engine)
# def get_session():
#     with Session(engine) as session:
#         yield session
# SessionDep = Annotated[Session, Depends(get_session)]
#
#
# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     create_db_and_models()
#     with Session(engine) as session:
#         if not session.exec(select(Campaign)).first():
#             session.add_all([
#                 Campaign(name="Summer Launch", due_date=datetime.now()),
#                 Campaign(name="Black_friday", due_date=datetime.now())
#             ])
#             session.commit()
#     yield
#


app = FastAPI(root_path="/api/v1")
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


