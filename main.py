#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello" : "world"}

# Request and Responde Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title= "Person Name",
        description= "This is the person name. It's between 1 and 50 characters"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )
):
    return {name: age}

# validaciones: path parameters

@app.get("/person/detail/{person_id}&{age}")
def show_person(
    person_id: int = Path(..., gt=0),
    age: int = Path(gt=17)
):
    return {person_id: "It exists", age: years old""}