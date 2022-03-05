import streamlit as st
import streamlit.components.v1 as components
from tempfile import SpooledTemporaryFile
from profanity_detector.spotify_func import SpotifyAPI
import pandas as pd
import altair as alt
import requests
import base64
import os
import streamlit.components.v1 as components
import json
from os import path
#from apps.home import input


client_id = 'de83171c026d4ca0b749e33b50496a60'
client_secret = '87a1f7300bf947fab323722e0418801f'


def app():
    st.title('SPOTIFY')

    if path.exists('movie.json'):
        movie_name = json.load(open('movie.json', 'r'))['movie']
        #st.write(movie_name)

    st.header(" :notes: Music ")
    st.subheader(" Spotify List")
    playlist_df = SpotifyAPI(client_id, client_secret).playlist_search_json_createdata(
            query=movie_name)
    top_playlist_id=playlist_df["ID"][0]
    components.html(f"""
                        <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{top_playlist_id}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
        """,
        height=400
                        )
