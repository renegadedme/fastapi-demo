from email import message
import dbmodels, schemas, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/vote",
    tags = ['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), authenticated_user = Depends(oauth2.get_current_user)):
    current_user = int(authenticated_user.id) #converts the current userid to an integer
    vote_query = db.query(dbmodels.Vote).filter(dbmodels.Vote.post_id == vote.post_id, dbmodels.Vote.user_id == current_user)
    found_vote = vote_query.first()
    post= db.query(dbmodels.Post).filter(dbmodels.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

        
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user} has already voted on post {vote.post_id}")
        new_vote = dbmodels.Vote(post_id = vote.post_id, user_id = current_user)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added"}
    
    if (vote.dir == 0):  
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found") 
        
        vote_query.delete(synchronize_session=False) 
        db.commit()

        return {"message": "Vote deleted"}
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Operation Not Supported")
