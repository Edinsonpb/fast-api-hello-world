#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import status
from fastapi import HTTPException

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

class PersonBase(BaseModel):
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


class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8
        )

class PersonOut(PersonBase):
    pass


    class Config:
        schema_extra = {
            "example": {
                "first_name": "Eva",
                "last_name": "Parra Buitrago",
                "age": 18,
                "hair_color": "black",
                "is_married": False,
                "password": "12345678"
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

class LoginOut(BaseModel):
    username: str = Field(...,
    max_length=20,
    example="12345678"
    )
    message: str = Field(default="Login Succesfull")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello" : "world"}

# Request and Responde Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters:
    - Reques body parameter:
        - **person: person** -> A person model with first name, last name, age, har color and marital status

    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title= "Person Name",
        description= "This is the person name. It's between 1 and 50 characters",
        example="Lorena"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=32
        )
):
    return {name: age}

# validaciones: path parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail/{person_id}&{age}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(..., gt=0),
    age: int = Path(gt=17)
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )
    return {person_id: "It exists", age: "years old"}

# Validaciones: request body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=1089603058
        ),
    person: Person = Body(...),
    location: Location = Body(...),
    personalcontact: Contactinfo = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    results.update(personalcontact.dict())
    return results

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(username: str = Form(...),
    password: str = Form(...)):
    return LoginOut(username=username)

#cookies and headers parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str =Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent
@app.post(
    path="/post-image"
)
def post_imaage(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=0)
    }