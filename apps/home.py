import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from profanity_detector.giphy import get_giphy
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.get_data import movie_data
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
import streamlit.components.v1 as components
from profanity_detector.spotify_func import SpotifyAPI
import json
from os import path
from profanity_detector.geo_data import get_max_country, enrich_locations, plot_location_map
from streamlit_folium import folium_static
import os
from dotenv import load_dotenv



st.set_page_config(page_icon="film_frames",
                   layout="wide",
                   initial_sidebar_state="expanded")


# Loading API_keys
load_dotenv()
if 'client_id' in os.environ:
    client_id = os.getenv('client_id')
else:
    client_id = os.environ['client_id']

if 'client_secret' in os.environ:
    client_secret = os.getenv('client_secret')
else:
    client_secret = os.environ['client_secret']



@st.cache
def load_data(movie_name):
    return movie_data(movie_name)


@st.cache(allow_output_mutation=True)
def geo_data(locations_df):
    locations_df = enrich_locations(locations_df)
    return locations_df


@st.cache
def data_reload():
    if path.exists('movie.json'):
        json.dump({'movie': ""}, open('movie.json', 'w'))


data_reload()

def app():

    st.title("IMBd - International Movie Bible Dashboard")
    st.header("Ready - Set - Action! :clapper: ")

    st.markdown('##')

    if path.exists('movie.json'):
        movie_name = json.load(open('movie.json', 'r'))['movie']
        movie_name = st.text_input(" What Is Your Favourite Movie ? : ", movie_name)
    else:
        movie_name = st.text_input(" What Is Your Favourite Movie ? : ", '')

    st.markdown('---')

    if movie_name:
        #get data
        json.dump({'movie': movie_name}, open('movie.json', 'w'))
        movie_meta, quotes_df, reviews_df, locations_df = load_data(movie_name)

        st.header(" :movie_camera: Movie Information ")
        col1, col2, col3 = st.columns(3)

        # -----SHOW METADATA ----------------------------
        with col1:
            st.subheader(f" Title: {movie_meta['title']}")
            st.image(movie_meta['cover_url'],
                    use_column_width='auto',
                    caption=movie_meta['title'])

        with col2:

            st.subheader(f":calendar: Year : {movie_meta['year']}")
            st.subheader(f":top: Ranking : {movie_meta['top_250_rank']}")
            st.subheader(
                f":moneybag: Box Office: US $ {movie_meta['box_office']}")
            st.subheader(f":star: Rating : {movie_meta['rating']}/10")


        with col3:
            st.subheader('Cast')
            with st.expander("See Cast List"):
                for member in movie_meta['cast']:
                    st.text(member)

            st.subheader('Director')
            with st.expander("See Directors List"):
                for director in movie_meta['director']:
                    st.text(director)

        st.markdown('---')

        st.header(" :smile: Most Popular Gifs")

        #-------------GIPHYS--------------------------

        col4, col5, col6, col7, col8 = st.columns(5)

        movies = get_giphy(movie_name)
        with col4 :
            st.markdown(
                    "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
                    .format(movies[0]),
                    unsafe_allow_html=True)

        with col5 :
            st.markdown(
                    "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
                    .format(movies[1]),
                    unsafe_allow_html=True)
        with col6 :
            st.markdown(
                    "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
                    .format(movies[2]),
                    unsafe_allow_html=True)

        with col7 :
            st.markdown(
                    "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
                    .format(movies[3]),
                    unsafe_allow_html=True)

        with col8 :
            st.markdown(
                    "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
                    .format(movies[4]),
                    unsafe_allow_html=True)


        st.markdown('---')

        col_left, col_right = st.columns([1,1])

        # # -------------- MUSIC ---------------


        with col_left:
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

        # ----------------MOVIE LOCATIONS---------------
        with col_right:
            st.header(" :round_pushpin: Locations ")
            st.subheader("Countries")
            with st.expander("See Countries"):
                for country in movie_meta['countries']:
                    st.text(country)

            st.subheader(" Filming Locations")
            location_df_new= geo_data(locations_df)
            country = get_max_country(location_df_new)
            map = plot_location_map(location_df_new, country)
            folium_static(map)
            st.markdown('---')
