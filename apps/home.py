import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from profanity_detector.giphy import get_giphy
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.get_data import movie_data
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.geo_data import enrich_locations


st.set_page_config(page_icon="film_frames",
                   layout="wide",
                   initial_sidebar_state="expanded")


#@st.cache
def app():
    st.title("IMBd - International Movie Bible Dashboard")
    st.header("Ready - Set - Action! :clapper: ")

    st.markdown('##')
    movie_name = st.text_input(" What Is Your Favourite Movie ? : ",
                               '')
    st.markdown('---')


    if movie_name:
        #get data
        movie_meta, quotes_df, reviews_df, locations_df = movie_data(movie_name)

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

        # -------------GIPHYS--------------------------

        # col4, col5, col6, col7, col8 = st.columns(5)

        # movies = get_giphy(movie_name)
        # with col4 :
        #     st.markdown(
        #             "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
        #             .format(movies[0]),
        #             unsafe_allow_html=True)

        # with col5 :
        #     st.markdown(
        #             "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
        #             .format(movies[1]),
        #             unsafe_allow_html=True)
        # with col6 :
        #     st.markdown(
        #             "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
        #             .format(movies[2]),
        #             unsafe_allow_html=True)

        # with col7 :
        #     st.markdown(
        #             "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
        #             .format(movies[3]),
        #             unsafe_allow_html=True)

        # with col8 :
        #     st.markdown(
        #             "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>"
        #             .format(movies[4]),
        #             unsafe_allow_html=True)


        st.markdown('---')



        # ----------------MOVIE LOCATIONS---------------

        col_left, col_right = st.columns([2,1])

        with col_left:
            st.header(" :round_pushpin: Locations ")
            st.subheader("Countries")
            with st.expander("See Countries"):
                for country in movie_meta['countries']:
                    st.text(country)

            st.subheader(" Filming Locations")
            # movie_locations = enrich_locations(locations_df)
            # st.map(movie_locations)
            # st.markdown('---')

        with col_right:
            st.header(" :notes: Music ")
            st.subheader(" Spotify List")










#     st.header("QuoteCloud")
#     plot_word_cloud(create_word_cloud(quotes_df))
#     st.pyplot()
