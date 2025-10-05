# FastAPI To-Do App

This is a simple To-Do application built using **FastAPI**.  
It allows users to **create, read, update, and delete tasks** using a RESTful API.

## Features
- Add a new task (POST /task)
- View all tasks (GET /tasks)
- View a single task by ID (GET /task/{id})
- Update a task (PUT /task/{id})
- Delete a task (DELETE /task/{id})

## Technology
- Python 3.x
- FastAPI
- Pydantic (for data validation)
- Uvicorn (for running the server)

You can interact with the API directly using the Swagger UI.

## Notes
- Tasks are stored **in memory** (Python list), so all data will be lost when the server restarts.
- Each task has the following structure:
```
json
{
 "id": 1,
 "name": "Task Name",
 "content": "Task details",
 "completed": false
}
```
