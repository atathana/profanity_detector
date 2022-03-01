import streamlit as st
from tempfile import SpooledTemporaryFile
import streamlit as st
from profanity_detector.spotify_func import SpotifyAPI
import pandas as pd
import altair as alt
import requests
import base64
import os

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
client_id ="1c87362eaaab48df92d5a6a4ef5f41be"
client_secret="851652f111714e2a959777fccf7ccc58"
spotify = SpotifyAPI(client_id, client_secret)

# movies = get_giphy(movie_name)
# print(movies)

# for movie in movies:
#     st.markdown(
#         "<iframe src= {} width='480' height='360' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>".format(movie),
#         unsafe_allow_html=True)

#spotify get movie name
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# local_css("style.css")

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
    need.append((i, track['artists'][0]['name'], track['name'], track_id, song_name, track['release_date'], popularity))

#data frame top10
Track_df = pd.DataFrame(need, index=None, columns=('Item', 'Artist', 'Album Name', 'Id', 'Song Name', 'Release Date', 'Popularity'))

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
chart_df = Sort_DF[['Artist', 'Album Name', 'Song Name', 'Release Date', 'Popularity',"energy"]]

Name_of_Feat="energy"
st.header(f"Popularity+Energy Chart")

c = alt.Chart(chart_df).mark_circle().encode(
    alt.X('Popularity', scale=alt.Scale(zero=False)), y=f'{Name_of_Feat}', color=alt.Color('Popularity', scale=alt.Scale(type='log',scheme='rainbow')), 
    size=alt.value(300), tooltip=['Popularity', f'{Name_of_Feat}', 'Song Name', 'Album Name']).interactive()

st.altair_chart(c, use_container_width=True)
st.header(f"{Name_of_Movie} Track List")
st.table(chart_df)