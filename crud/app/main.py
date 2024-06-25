from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from contextlib import asynccontextmanager


from sqlmodel import Session,select
from app.model.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from app.database.connection import get_db, create_db_and_tables
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Todo App")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["*"],
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"]
# )

@app.post("/todos", response_model=TodoRead)
def create_todo(todo: TodoCreate, db:Annotated[Session, Depends(get_db)])->Todo:
    # print("Data from client:", todo)
    todo_insert = Todo.model_validate(todo)
    print("Data after validatoin:", todo_insert)
    db.add(todo_insert)
    db.commit()
    db.refresh(todo_insert)
    return todo_insert

@app.get("/todos", response_model=list[TodoRead])
def get_todos(db:Annotated[Session, Depends(get_db)]):
    todos = db.exec(select(Todo)).all()
    return todos

@app.get("/todos/{todo_id}", response_model=TodoRead)
def get_todo_by_id(todo_id:int, db:Annotated[Session, Depends(get_db)])->Todo:
    todo = db.exec(select(Todo).where(Todo.id == todo_id)).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id:int, todo_data:TodoUpdate, db:Annotated[Session, Depends(get_db)])->Todo:
    todo = db.exec(select(Todo).where(Todo.id == todo_id)).one()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    print("Todo in DB:", todo)
    print("Data from client:", todo_data)

    todo_data_dict = todo_data.model_dump(exclude_unset=True)
    print("Todo in DICT:", todo_data_dict)

    for key, value in todo_data_dict.items():
        setattr(todo, key, value)
    print("Todo after update:", todo)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int, db:Annotated[Session, Depends(get_db)]):
    try:
        todo =  db.exec(select(Todo).where(Todo.id == todo_id)).one()
        db.delete(todo)
        db.commit()
    except:
        db.rollback()
        return {"message": "Error deleting todo"}
    
    return {"message": "Todo deleted successfully"}

