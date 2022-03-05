import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from profanity_detector.spotify_func import SpotifyAPI
import streamlit.components.v1 as components
import os

from dotenv import load_dotenv
load_dotenv()
if 'client_id' and 'client_secret'in os.environ:
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
else:
    client_id = os.environ('client_id')
    client_secret = os.environ('client_secret')


st.set_page_config(page_title="I m BD",
                   page_icon="film_frames",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.title('I m BD')
st.text('International Movie Bible Dashboard')
#get movie name


movie_name = st.text_input("What Is Your Favourite Movie? : ", '')
if movie_name:
    
    #"""please copy and paste in app.py """
    playlist_df=SpotifyAPI(client_id,client_secret).playlist_search_json_createdata(query="titanic")
    top_playlist_id=playlist_df["ID"][0]
    
    st.title("Playlist Search Result")
    components.html(
            f"""
            
            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{top_playlist_id}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                """,
                height=400
            ) 
    #----------------------------------------
