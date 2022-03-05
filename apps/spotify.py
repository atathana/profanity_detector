import streamlit as st
from profanity_detector.spotify_func import SpotifyAPI
import streamlit.components.v1 as components

def app():
    st.title('Spotify')
    uri=spotify_get_data["albumID"][0]
    components.html(
                f"""
                <iframe src=https://open.spotify.com/embed/album/{uri} width="200" height="500" frameborder="50" allowtransparency="true"
                allow="encrypted-media" ></iframe
                    """,
                    height=400
                )

    st.write("This is the `Data` page of the multi-page app.")
