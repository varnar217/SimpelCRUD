from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, Base, engine
# from schemas import TaskFactory
from models import Task
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base.metadata.create_all(bind=engine)
# # Pydantic модель для запросов
class TaskCreate(BaseModel):
    name: str

@app.post("/tasks/", response_model=None)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Конечная точка для извлечения одного элемента "Task" по id
@app.get("/task/{task_id}", response_model=None)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Конечная точка для обновления элемента "Task" по id
class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool

@app.put("/task/{task_id}", response_model=None)
async def update_task(task_id: int, todo: TaskUpdate, db: Session = Depends(get_db)):
    task_db = db.query(Task).filter(Task.id == task_id).first()
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db.title = todo.title
    task_db.description = todo.description
    task_db.completed = todo.completed
    db.commit()
    db.refresh(task_db)
    return task_db

# Конечная точка для удаления элемента "Task" по id
@app.delete("/task/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)