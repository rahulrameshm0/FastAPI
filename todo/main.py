from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
app = FastAPI()


class Task(BaseModel):
    name: str
    content: str
    completed: bool = True


tasks: List[Task] = []
@app.post('/task')
async def create_task(task: Task):
    tasks.append(task)
    return {"Message":"task added successfully", "Task":tasks}

@app.get('/tasks/')
async def get_tasks():
    return tasks

@app.get('/task/{task_id)}')
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
        raise HTTPException(status_code=404, detail="Id is not found")
@app.put('/task/{task_id}')
async def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return {"message":"task updated successfully", "task":updated_task}
        raise HTTPException(status_code=404, detail="id not found")

@app.delete('/task/{task_id}')
async def delete_task(task_id:int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del_task = tasks.pop(i)
            return {"message": "task deleted successfully", "task":del_task}
        raise HTTPException(status_code=404, detail="id not found")
