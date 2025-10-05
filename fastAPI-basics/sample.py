from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(root_path="/api/v1")

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Operation(BaseModel):
    value: list
    operation: str


@app.post('/operation')
async def operation(data: Operation):
    value = data.value
    op = data.operation.lower()

    if op == "+":
        result = value[0] + value[1]
    elif op == "-":
        result = value[0] - value[1]
    elif op == "*":
        result = value[0] * value[1]
    elif op == "/":
        if value[1] == 0:
            return f"{value[1]} is not divisible!"
        result = value[0] / value[1]
    else:
        return "There is no such operation like this!"

    return {"Total": result}




