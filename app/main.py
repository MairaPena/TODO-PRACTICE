from typing import Dict

import pydantic
import uvicorn
from fastapi import FastAPI

from app import services
from app.adapters import DatabaseAdapter

# Create an instance of the FastAPI class
app = FastAPI()

# Set up the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
DatabaseAdapter(db_url=SQLALCHEMY_DATABASE_URL)


# Define a route for the /get_task_by_id endpoint
@app.get("/get_task_by_id/{task_id}", status_code=200)
def get_task_by_id(task_id: str) -> Dict:
    return services.get_task_by_id(task_id=task_id, db=DatabaseAdapter())  # type: ignore


@app.get("/get_all_tasks", status_code=200)
def get_all_tasks() -> list[Dict]:
    return services.get_all_tasks(db=DatabaseAdapter())


class Response(pydantic.BaseModel):
    task_id: str


# Define a route for the /create_task endpoint
@app.post("/create_task", status_code=201)
def create_task(task: Dict) -> dict:
    id_ = services.create_task(task=task, db=DatabaseAdapter())
    return Response(task_id=id_).model_dump()


if __name__ == "__main__":  # Only input dev
    uvicorn.run(app, host="0.0.0.0", port=8080)
