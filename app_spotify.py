import streamlit as st
from tempfile import SpooledTemporaryFile
import streamlit as st
from profanity_detector.spotify_func import SpotifyAPI
import pandas as pd
import altair as alt
import requests
import base64
import os
import streamlit.components.v1 as components
from IPython.core.display import display, HTML
from streamlit_player import st_player



#To do 
#get os.environ.get
#git conflicts :push all?
#combine into app.py to the latest one
#need from dotenv import load_dotenv?
# make classs and make it compact ,import python file as class 
#play music features??
#connect to the devise

# client_id = os.environ.get("CLIENTID")
# client_secret=os.environ.get("CLIENTSEC")
client_id ="5c89e3fbc1514489ba396629b99ead14"
client_secret="ff02150e1f764930be352d8789f1067b"
spotify = SpotifyAPI(client_id, client_secret)

#Menu
# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")


#title,icon
components.html(
    """
 <img src="https://img.icons8.com/ultraviolet/80/000000/spotify--v2.png"/>
    """,height=100
)
st.title("Spotify List")


#movie name
Name_of_Movie = st.text_input("Movie Name")


#Start Data  or you can use class potify.spotify_get_organised_data func from spotify_func.py
Data = spotify.search({"album": f"{Name_of_Movie}"}, search_type="track")
#need contents 
need = []
for i, item in enumerate(Data['tracks']['items']):
    track = item['album']
    track_id = item['id']
    song_name = item['name']
    popularity = item['popularity']
    need.append((i, track['artists'][0]['name'], track['name'], track_id, song_name, track['release_date'], popularity,item['album']["id"]))

#data frame top10
Track_df = pd.DataFrame(need, index=None, columns=('Item', 'Artist', 'Album Name', 'Id', 'Song Name', 'Release Date', 'Popularity',"albumID"))

access_token = spotify.access_token
headers = {
    "Authorization": f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/audio-features/"

#Full data
Feat_df = pd.DataFrame()
for id in Track_df['Id'].iteritems():
    track_id = id[1]
    lookup_url = f"{endpoint}{track_id}"
    ra = requests.get(lookup_url, headers=headers)
    audio_feat = ra.json()
    Features_df = pd.DataFrame(audio_feat, index=[0])
    Feat_df = Feat_df.append(Features_df)
Full_Data = Track_df.merge(Feat_df, left_on="Id", right_on="id")

#END data sort
Sort_DF = Full_Data.sort_values(by=['Popularity'], ascending=False).head(10)




#chart df 
chart_df = Sort_DF[['Artist', 'Album Name', 'Song Name', 'Release Date', 'Popularity',"energy","albumID"]]
Name_of_Feat="energy"

#chart df drop deplicate
drop_deplicated_data=chart_df.drop_duplicates(subset=['Album Name'], keep="first").reset_index(drop=True)


#chart
st.header(f"Popularity+Energy Chart")
c = alt.Chart(chart_df).mark_circle().encode(
    alt.X('Popularity', scale=alt.Scale(zero=False)), y=f'{Name_of_Feat}', color=alt.Color('Popularity', scale=alt.Scale(type='log',scheme='rainbow')), 
    size=alt.value(300), tooltip=['Popularity', f'{Name_of_Feat}', 'Song Name', 'Album Name']).interactive()

st.altair_chart(c, use_container_width=True)


#player show
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

             <iframe src=https://open.spotify.com/embed/album/{uri1} width="230" height="500" frameborder="50" allowtransparency="true" 
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


#show data table
st.header(f"{Name_of_Movie} Track List")
st.table(chart_df)





