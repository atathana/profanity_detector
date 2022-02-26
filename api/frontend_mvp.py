from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from profanity_detector.get_data import movie_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/display_movie_data")
def display_movie_data(movie_name):
    meta, quotes, reviews, locations = movie_data(movie_name)
    cover = meta["cover_url"]
    return {"movie_details": meta,
            }