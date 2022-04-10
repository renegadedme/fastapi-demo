import dbmodels, schemas, utils
from sqlalchemy.orm import Session
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from database import get_db
from typing import List 

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

#CREATE USER:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserResponse)
#define the function that accepts 2 variables - 'user' as a pydantic model object and db as a database session
def create_posts(user: schemas.CreateUser, db: Session = Depends(get_db)):

    #hash the user's password:
    hashed_password = utils.hash(user.password)  #referencing the password hash function
    user.password = hashed_password
    #to add a user, the pydantic object (user) must be converted to a dictionary using the .dict() method
    new_user = dbmodels.User(**user.dict())   #unpacking the fields of a user and assigning it to a new variable
    db.add(new_user)  #adds the new user to the database
    db.commit()       #commmits the changes
    db.refresh(new_user)
    return new_user


#GET ALL USERS:
@router.get("/", response_model=List[schemas.CreateUserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(dbmodels.User).all()
    return users 


#GET A USER BY ID:
@router.get("/{id}", response_model=schemas.CreateUserResponse)
#define the function that accepts 2 variables - id as an integer and db as a database session
def get_user(id:int, db: Session = Depends(get_db)):
    #query the User table for the first record where the requested user id matches an id in the DB
    user = db.query(dbmodels.User).filter(dbmodels.User.id == id).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid user ID")
    return user