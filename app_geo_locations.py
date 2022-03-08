import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from profanity_detector.get_data import movie_data
from profanity_detector.geo_data import geo_map_main, geo_map_countries
from streamlit_folium import folium_static
import folium


st.set_page_config(page_title="I m BD",
                   page_icon="film_frames",
                   layout="wide",
                   initial_sidebar_state="expanded")


st.title('Movie Scene Set Locations')

movie_name = st.text_input("What Is Your Favourite Movie? : ", '')

if movie_name:

    

    #get data
    movie_meta, quotes_df, reviews_df, locations_df = movie_data(movie_name)

    st.header ("All Locations By Country")
    country_maps = geo_map_countries(locations_df)

    
    for country in country_maps:
        st.subheader(country)
        show_map = folium_static(country_maps[country])
        st.markdown(
            "<iframe title={} src= {} width='240' height='180' frameBorder='0' allowFullScreen></iframe>".format(country ,show_map),
             unsafe_allow_html=True)