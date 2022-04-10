from fastapi import FastAPI
import dbmodels
from database import engine
from routers import posts, users, auth, vote
from config import settings
from fastapi.middleware.cors import CORSMiddleware


dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


#define origins
#for specific use-cases, define an actual list of origins
origins = [
    "*"
]

#define CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#ROOT:
@app.get("/")
def root():
    return {"message": "Welcome"}





