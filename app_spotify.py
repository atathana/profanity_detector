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
client_id ="a2a39f20a23a41fa94057a7e2cb13675"
client_secret="4dc99bfd287e44b8bde2cab06d4b3e05"
spotify = SpotifyAPI(client_id, client_secret)

#Menu
# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# Space out the maps so the first one is 2x the size of the other three


#title,icon
components.html(
    """
 <img src="https://img.icons8.com/ultraviolet/80/000000/spotify--v2.png"/>
 
    """,height=100
)
st.title("Spotify List")


Name_of_Movie = st.text_input("Movie Name")

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

#sort
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



#player loop
st.title("Music Gallery")
st.title(len(drop_deplicated_data["albumID"]))
i=0
while i < len(drop_deplicated_data["albumID"]):
# for i in range(0,len(drop_deplicated_data["albumID"]),2):
    uri=drop_deplicated_data["albumID"][i]
    uri1=drop_deplicated_data["albumID"][i+1]
     
    components.html(
   f"""
   <div style=”display: inline-block;”>
 <iframe src=https://open.spotify.com/embed/album/{uri} width="230" height="500" frameborder="50" allowtransparency="true" 
 allow="encrypted-media" ></iframe>
 
  <iframe src=https://open.spotify.com/embed/album/{uri1} width="230" height="500" frameborder="50" allowtransparency="true" 
 allow="encrypted-media" ></iframe>
 
    """,
    height=300,
)
    i=i+2
    
    
 #loop
 col1, col2= st.columns(2)
 for i in len(drop_deplicated_data["albumID"]):
         uri=drop_deplicated_data["albumID"][i]
    uri1=drop_deplicated_data["albumID"][i+1]
 with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")
   

# uri=chart_df["albumID"].reset_index(drop=True)[0]
# components.html(
#    f"""
#  <iframe src=https://open.spotify.com/embed/album/{uri} width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
#     """,
#     height=200,
# )


#show table
st.header(f"{Name_of_Movie} Track List")
st.table(chart_df)




