import dbmodels, schemas, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)


#GET ALL POSTS:
@router.get("/", response_model=List[schemas.PostVote])
#@router.get("/")
#limit for limiting the number of entries at once, defaults to 10 in this case
#skip for skipping certain results, can be used for pagination by skipping based on the limit per page
def get_posts(db: Session = Depends(get_db), authenticated_user = Depends(oauth2.get_current_user), limit: int = 10, skip: int =0, search: Optional[str]= ""):
    #query the Post db table for all entries
    #posts = db.query(dbmodels.Post).filter(dbmodels.Post.title.contains(search)).limit(limit).offset(skip).all()
    #to only return the posts belonging to the logged in user:
    #current_user = int(authenticated_user.id)   #converts the current userid to an integer
    #posts = db.query(dbmodels.Post).filter(dbmodels.Post.owner_id == current_user).all()
    
    #Left Outer Join Query to Retrieve Post Including the Number of Votes It Has
    posts = db.query(dbmodels.Post, func.count(dbmodels.Vote.post_id).label("votes")).join(dbmodels.Vote, dbmodels.Vote.post_id == dbmodels.Post.id, isouter=True).group_by(dbmodels.Post.id).filter(dbmodels.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

#GET A POST BY ID:
#define the route and the response
@router.get("/{id}", response_model=schemas.PostVote)

#define the function that accepts variables - post id as an integer and db as a database session
def get_post(id:int, db: Session = Depends(get_db), authenticated_user = Depends(oauth2.get_current_user)):
    
    #query to retrieve the post
    post = db.query(dbmodels.Post, func.count(dbmodels.Vote.post_id).label("votes")).join(dbmodels.Vote, dbmodels.Vote.post_id == dbmodels.Post.id, isouter=True).group_by(dbmodels.Post.id).filter(dbmodels.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    #Authorization Logic to ensure a user can only delete their own post(s):
    #current_user = int(authenticated_user.id)        #convert the current userid to an integer
    #if post.owner_id != current_user:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to access this post") 

    return post


#ADD A POST:
#define the route, the default status code and response
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)

#allow creation of posts only if the caller is authenticated.
#this calls the get_current_user function which calls the verify_access_token function
def create_posts(newpost: schemas.CreatePost, db: Session = Depends(get_db), authenticated_user = Depends(oauth2.get_current_user)):
    current_user = int(authenticated_user.id) #converts the current userid to an integer
    
    #newpost is a pydantic model object and needs to be converted to a dictionary
    post = dbmodels.Post(owner_id=current_user, **newpost.dict())   #unpacking the fields of a post for dynamic assignment
    db.add(post)   #adds the new post to the database
    db.commit()
    db.refresh(post)
    return post
   

#DELETE A POST:
#define the route and the default status code 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), authenticated_user = Depends(oauth2.get_current_user)):
    current_user = int(authenticated_user.id)   #converts the current userid to an integer
    post_query = db.query(dbmodels.Post).filter(dbmodels.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    #Authorization Logic to ensure a user can only delete their own post(s):
    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to delete this post")  
     
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#UPDATE A POST:
#define the route and the response
@router.put("/{id}", response_model=schemas.PostResponse)

def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), authenticated_user = Depends(oauth2.get_current_user)):
    current_user = int(authenticated_user.id) #converts the current userid to an integer
    #query the User table for the first record where the requested user id matches an id in the DB:
    post_query = db.query(dbmodels.Post).filter(dbmodels.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} does not exist")
    
    #Authorization Logic to ensure a user can only update their own post(s):
    if post.owner_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to update this post")   

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()