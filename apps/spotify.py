import streamlit as st
import streamlit.components.v1 as components
from tempfile import SpooledTemporaryFile
from profanity_detector.spotify_func import SpotifyAPI
import pandas as pd
import altair as alt
import json
from os import path
from dotenv import load_dotenv
import os


load_dotenv()
if 'client_id' in os.environ:
    client_id = os.getenv('client_id')
else:
    client_id = os.environ['client_id']

if 'client_secret' in os.environ:
    client_secret = os.getenv('client_secret')
else:
    client_secret = os.environ['client_secret']

#instanciate class
spotify = SpotifyAPI(client_id, client_secret)
def app():

    st.title(' :notes: MUSIC')

    if path.exists('movie.json'):
        movie_name = json.load(open('movie.json', 'r'))['movie']

    if movie_name:

        #chart df drop deplicate
        # drop_deplicated_data = chart_df.drop_duplicates(subset=['Album Name'], keep="first").reset_index(drop=True)

        playlist_df=spotify.playlist_search_json_createdata(query=movie_name)
        top_playlist_id=playlist_df["ID"][0]

        col_left, col_right = st.columns([1,2])

        with col_left:
            st.subheader(" Spotify List")

            components.html(
                f"""

                <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{top_playlist_id}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                    """,
                    height=400
                )
            #playlist table
            with st.expander("15 Alternative Playlists"):
                st.table(playlist_df[["Name"]].head(15))

        with col_right:
            #song chart
            st.subheader(f"Energy vs Popularity")
            st.text(
                """
                Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity.
                Typically, energetic tracks feel fast, loud, and noisy.
                Perceptual features contributing to this attribute include dynamic range, perceived loudness,
                timbre, onset rate, and general entropy.
                """
            )

            Name_of_Feat = "energy"
            playlist_link = playlist_df["PlaylistURL"][0]
            track_df = spotify.get_track_from_playlist(playlist_link)

            chart_df = track_df[["album", "track_name", "popularity", "energy"]]

            c = alt.Chart(chart_df[["album", "track_name", "popularity",
                                    "energy"]]).mark_circle().encode(
                                        alt.X('popularity', scale=alt.Scale(zero=False)),
                                        y=f'{Name_of_Feat}',
                                        color=alt.Color('popularity',
                                                        scale=alt.Scale(type='log',
                                                                        scheme='rainbow')),
                                        size=alt.value(600),
                                        tooltip=[
                                            'track_name', 'popularity', f'{Name_of_Feat}',
                                            "energy"
                                        ]).interactive()

            st.altair_chart(c, use_container_width=True)

            #song table
            with st.expander("See more Track List"):
                st.table(chart_df)
