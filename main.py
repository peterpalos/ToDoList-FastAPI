from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import select
from .database import *
from .models import *


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


### ToDo apps

@app.post("/todos/", response_model=ToDoRead)
def create_ToDo(*, session: Session = Depends(get_session), todo: ToDoCreate):
    accepted_priorities = ["low", "normal", "high"]
    if todo.priority.lower() not in accepted_priorities:
        raise HTTPException(status_code=404, detail="Choose priority from {}".format(accepted_priorities))

    db_todo = ToDo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/todos/", response_model=List[ToDoRead])
def read_ToDo_list(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    todos = session.exec(select(ToDo).offset(offset).limit(limit)).all()
    return todos


@app.get("/todos/{todo_id}", response_model=ToDoReadWithProject)
def read_specific_ToDo(*, session: Session = Depends(get_session), todo_id: int):
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo


@app.patch("/todos/{todo_id}", response_model=ToDoRead)
def update_ToDo(
    *, session: Session = Depends(get_session), todo_id: int, todo: ToDoUpdate
):
    db_todo = session.get(ToDo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_ToDo(*, session: Session = Depends(get_session), todo_id: int):

    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}


### Project apps

@app.post("/projects/", response_model=ProjectRead)
def create_project(*, session: Session = Depends(get_session), project: ProjectCreate):
    db_project = Project.from_orm(project)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@app.get("/projects/", response_model=List[ProjectRead])
def read_project_list(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    projects = session.exec(select(Project).offset(offset).limit(limit)).all()
    return projects


@app.get("/projects/{project_id}", response_model=ProjectReadWithToDos)
def read_specific_project(*, project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    *,
    session: Session = Depends(get_session),
    project_id: int,
    project: ProjectUpdate,
):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_data = project.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@app.delete("/projects/{project_id}")
def delete_project(*, session: Session = Depends(get_session), project_id: int):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"ok": True}
