from os import access
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
import dbmodels, schemas, utils, oauth2


router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login', response_model=schemas.Token)
#define the login function which takes the user's credentials and the database session
#the user credentials are stored in a form which outputs the entries as "username" and "password"

def login(user_creds: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    #verify that the provided email matches an email in the database. The email field is represented as "username"
    user = db.query(dbmodels.User).filter(dbmodels.User.email == user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    #compare provided password with the user's password
    password = utils.verify(user_creds.password, user.password)
    if not password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "email": user.email})
    return{"access_token": access_token, "token_type": "Bearer", "user_id": user.id}