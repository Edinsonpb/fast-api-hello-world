#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        max_length=20
    )
    state: str = Field(
        ...,
        max_length=20
    )
    country: str = Field(
        ...,
        max_length=20
    )

    class Config:
        schema_extra = {
            "example": {
                "city": "Pereira",
                "state": "Risaralda",
                "country": "Colombia"
            }
        }


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name:  str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=17,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Eva",
                "last_name": "Parra Buitrago",
                "age": 18,
                "hair_color": "black",
                "is_married": False
            }
        }

class Contactinfo(BaseModel):
    personalemail: EmailStr = Field(default=None)
    cellphone: str = Field(
        ...,
        min_length=10
    )

    class Config:
        schema_extra = {
            "example": {
                "personalemail": "evaparrabuitrago@gmail.com",
                "cellphone": "3174341284"
            }
        }


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
    return {person_id: "It exists", age: "years old"}

# Validaciones: request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...),
    personalcontact: Contactinfo = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    results.update(personalcontact.dict())
    return results