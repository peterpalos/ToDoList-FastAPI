# ToDo List app

A small project to demonstrate the use of [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/)

## Required packages
  * Python 3.6+
  * [FastAPI](https://fastapi.tiangolo.com/) 
  * [SQLModel](https://sqlmodel.tiangolo.com/)
  * [Uvicorn](https://www.uvicorn.org/)

## Features

The app provides the most necessary options for organizing your daily tasks

**You have task functions**:
  * Add
  * Modify
  * Delete
  * Read a task
  * Read the Todo list

**And project functions to organize the tasks into larger modules**
  * Add
  * Modify
  * Delete
  * Read a project
  * Read the project list
##
**A task has 6 attributes**
  * ID (int) - automatically generated, cannot be modified
  * Name of the task (str)
  * The project where it is classified (str)
  * Priority (low, normal, high)
  * Deadline (date)
  * Done (bool) - False automatically generated, can be modified later
  
**A project has 4 attributes**
  * ID (int) - automatically generated, cannot be modified
  * Name of the project (str)
  * Name of the project manager (str)
  * Department (str)
  
You can read a specific project to get the related tasks - For transparency reasons, they do not appear in the full project listing

## Structure

``` 
├── README.md
├── todoapp
    ├── __init__.py ............... 1.
    ├── database.db ............... 2.
    ├── database.py ............... 3.
    ├── main.py ................... 4.
    └── models.py ................. 5.
```
where the
* database object contains a sample ToDo list
* database module creates the engine and the function to create all the tables
* main module contains the path operations
* models module contains the database models (schemas)

## Quick start
```bash
$ uvicorn todoapp.main:app
```
**Interactive API documentation at:** http://127.0.0.1:8000/docs
