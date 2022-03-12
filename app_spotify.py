import streamlit as st
from tempfile import SpooledTemporaryFile
from profanity_detector.spotify_func import SpotifyAPI,client_id,client_secret
import pandas as pd
import altair as alt
import requests
import base64
import os
import streamlit.components.v1 as components
from IPython.core.display import display, HTML
from streamlit_player import st_player

from dotenv import load_dotenv


#To do 
#get os.environ.get
#git conflicts :push all?
#combine into app.py to the latest one
#need from dotenv import load_dotenv?
# make classs and make it compact ,import python file as class 
#play music features??
#connect to the devise


# load_dotenv()
# if 'client_id' and 'client_secret'in os.environ:
#     client_id = os.getenv('client_id')
#     client_secret = os.getenv('client_secret')
# else:
#     client_id = os.environ('client_id')
#     client_secret = os.environ('client_secret')

#Menu wide
st.set_page_config(layout="wide")

#title,icon
components.html(
    """
 <img src="https://img.icons8.com/ultraviolet/80/000000/spotify--v2.png"/>
    """,height=100
)
st.title("Spotify List")


#put movie name
Name_of_Movie = st.text_input("Movie Name")

#instanciate class 
spotify=SpotifyAPI(client_id,client_secret)

#get organised data 
chart_df=spotify.spotify_get_organised_data(Name_of_Movie)
#chart df drop deplicate
drop_deplicated_data=chart_df.drop_duplicates(subset=['Album Name'], keep="first").reset_index(drop=True)

#playlist player show
if Name_of_Movie:
    playlist_df=spotify.playlist_search_json_createdata(query=Name_of_Movie)
    top_playlist_id=playlist_df["ID"][0]
    
    st.title("No.1 Playlist Search Result")
    components.html(

            f"""
            
            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{top_playlist_id}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                """,
                height=400
            ) 
    #playlist table
    with st.expander("See Playlist List"):
        st.table(playlist_df[["Name","PlaylistURL"]])
        
    
else:
    playlist_df=spotify.playlist_search_json_createdata(query="titanic")
    top_playlist_id=playlist_df["ID"][0]
    
    st.title("No.1 Playlist Search Result")
    components.html(
            f"""
            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{top_playlist_id}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                """,
                height=400
            ) 
    #playlist table
    with st.expander("See Playlist List"):
        st.table(playlist_df[["Name","PlaylistURL"]])

# #show data table
st.header(f"{Name_of_Movie}  TOP 1 Playlist Track ")

#song chart
st.header(f"Song Popularity+Energy Chart")
Name_of_Feat="energy"
playlist_URI=playlist_df["PlaylistURL"][0]
track_df=SpotifyAPI.get_track_from_playlist(playlist_URI)
chart_df=track_df[["album","track_name","popularity","energy"]]

c = alt.Chart(chart_df[["album","track_name","popularity","energy"]]).mark_circle().encode(
    alt.X('popularity', scale=alt.Scale(zero=False)), y=f'{Name_of_Feat}', color=alt.Color('popularity', scale=alt.Scale(type='log',scheme='rainbow')), 
    size=alt.value(300), tooltip=['track_name','popularity', f'{Name_of_Feat}',"energy"]).interactive()
st.altair_chart(c, use_container_width=True)


#song table
with st.expander("See more Track List"):
    st.table(chart_df)

