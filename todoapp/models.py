from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import date

### Project classes
class ProjectBase(SQLModel):
    name: str
    manager: str
    department: str


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    todos: List["ToDo"] = Relationship(back_populates="project")


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int


class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    manager: Optional[str] = None
    department: Optional[str] = None


### ToDo classes
class ToDoBase(SQLModel):
    task: str
    project_name: Optional[str] = Field(default=None, foreign_key="project.name")
    priority: str = "normal"
    deadline: date


class ToDo(ToDoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project: Optional[Project] = Relationship(back_populates="todos")
    done: Optional[bool] = False


class ToDoRead(ToDoBase):
    id: int
    done: bool


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(SQLModel):
    task: Optional[str] = None
    project_name: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[date] = None
    done: Optional[bool] = None


### Two more classes to integrate cross-sectional data in specific ToDo or Project read

class ToDoReadWithProject(ToDoRead):
    projects: Optional[ProjectRead] = None


class ProjectReadWithToDos(ProjectRead):
    todos: List[ToDoRead] = []
