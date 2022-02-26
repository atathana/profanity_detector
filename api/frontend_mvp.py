from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from profanity_detector.get_data import get_all_movie_data,get_meta_data

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
    movie_data = get_all_movie_data(movie_name)
    movie_meta = get_meta_data(movie_data)
    return {"movie_details": movie_meta}