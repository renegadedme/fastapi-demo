from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr #importing the pydantic base model for defining the structure of requests/responses

#define the structure of a request/response

class UserBase(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True

class CreateUser(UserBase):
    password: str

class CreateUserResponse(UserBase):
    id: int
    created_at: datetime 
    class Config:
        orm_mode = True 

class UserLogin(UserBase):
    password: str

class PostBase(BaseModel):  
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime 
    owner_id: int
    owner: UserBase
    class Config:
        orm_mode = True 

class PostVote(BaseModel):
    Post: PostResponse
    votes: int 
    class Config:
        orm_mode = True 

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    class Config:
        orm_mode = True 

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int