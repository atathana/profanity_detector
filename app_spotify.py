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
    st.title("Playlist Search Result")
    components.html(
            f"""
            
            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{top_playlist_id}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                """,
                height=400
            ) 
    #playlist table
    with st.expander("See Playlist List"):
        st.table(playlist_df[["Name","PlaylistURL"]].head(30))
    
else:
    playlist_df=spotify.playlist_search_json_createdata(query="titanic")
    top_playlist_id=playlist_df["ID"][0]
    
    st.title("Playlist Search Result")
    components.html(
            f"""
            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{top_playlist_id}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                """,
                height=400
            ) 
    #playlist table
    with st.expander("See more Playlist"):
        st.table(playlist_df[["Name","PlaylistURL"]].head(10))


#show data table
st.header(f"{Name_of_Movie}  Song Search Result")

#song chart
st.header(f"Song Popularity+Energy Chart")
Name_of_Feat="energy"
c = alt.Chart(chart_df).mark_circle().encode(
    alt.X('Popularity', scale=alt.Scale(zero=False)), y=f'{Name_of_Feat}', color=alt.Color('Popularity', scale=alt.Scale(type='log',scheme='rainbow')), 
    size=alt.value(300), tooltip=['Popularity', f'{Name_of_Feat}', 'Song Name', 'Album Name']).interactive()
st.altair_chart(c, use_container_width=True)


#song table
with st.expander("See more Song List"):
    st.table(chart_df.head(10))

#Album player show
col1, col2,col3,col4= st.columns(4)
if len(drop_deplicated_data["albumID"]) == 1:
    with col3:
        uri=drop_deplicated_data["albumID"][0]
        components.html(
            f"""
            <iframe src=https://open.spotify.com/embed/album/{uri} width="200" height="400" frameborder="50" allowtransparency="true" 
            allow="encrypted-media" ></iframe>
                """,
                height=400
            ) 
    with col2:
        components.html(
            f"""
           <img  src="https://img.icons8.com/external-xnimrodx-lineal-gradient-xnimrodx/64/000000/external-audio-online-learning-xnimrodx-lineal-gradient-xnimrodx.png"/>
                """,
                height=300
            ) 
elif len(drop_deplicated_data["albumID"]) > 1:
    with col2:
        uri=drop_deplicated_data["albumID"][0]
        components.html(
            f"""
            <iframe src=https://open.spotify.com/embed/album/{uri} width="200" height="500" frameborder="50" allowtransparency="true" 
            allow="encrypted-media" ></iframe>
                """,
                height=400
            )    
    with col3:
        uri1=drop_deplicated_data["albumID"][1]
        components.html(
            f"""
            <iframe src=https://open.spotify.com/embed/album/{uri1} width="200" height="500" frameborder="50" allowtransparency="true" 
            allow="encrypted-media" ></iframe>
                """,
                height=400,
            )
    with col1:
        components.html(
            f"""
            <div style="text-align: center;">
            <img src="https://img.icons8.com/external-xnimrodx-lineal-gradient-xnimrodx/64/000000/external-audio-online-learning-xnimrodx-lineal-gradient-xnimrodx.png"/>
            </div>
                """,
                height=100
            ) 
        components.html(
            f"""
            <img src="https://img.icons8.com/external-tulpahn-flat-tulpahn/64/000000/external-audio-mobile-user-interface-tulpahn-flat-tulpahn.png"/>
                """,
                height=100
            ) 
        with col4:
            components.html(
            f"""
            <div style="margin-left:30px;">
            <img src="https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/000000/external-audio-edm-flaticons-lineal-color-flat-icons-2.png"/>
            </div>
                """,
                height=100
            )    
            components.html(
            f"""
            <div style="text-align: right;">
            <img src="https://img.icons8.com/external-tulpahn-flat-tulpahn/64/000000/external-audio-mobile-user-interface-tulpahn-flat-tulpahn.png"/>
            </div>
                """,
                height=100
            ) 
elif len(drop_deplicated_data["albumID"]) == 0:
    None
    
else:
    None

