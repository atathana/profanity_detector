import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from profanity_detector.spotify_func import SpotifyAPI
import streamlit.components.v1 as components
import os

from dotenv import load_dotenv

load_dotenv()
if 'client_id' and 'client_secret' in os.environ:
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
else:
    client_id = os.environ('client_id')
    client_secret = os.environ('client_secret')


# client_id = 'de83171c026d4ca0b749e33b50496a60'
# client_secret = '87a1f7300bf947fab323722e0418801f'

st.set_page_config(page_title="I m BD",
                   page_icon="film_frames",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.title('I m BD')
st.text('International Movie Bible Dashboard')
#get movie name


movie_name = st.text_input("What Is Your Favourite Movie? : ", '')
if movie_name:
    uri=SpotifyAPI(client_id,client_secret).spotify_get_organised_data(Name_of_Movie=movie_name)["albumID"][0]
    components.html(
            f"""
            <iframe src=https://open.spotify.com/embed/album/{uri} width="400" height="500" frameborder="50" allowtransparency="true"
            allow="encrypted-media" ></iframe>
                """,
                height=500
            )
