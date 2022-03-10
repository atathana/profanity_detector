import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from profanity_detector.get_data import movie_data
from profanity_detector.geo_data import enrich_locations,plot_location_map
from streamlit_folium import folium_static
import folium
import json
from os import path


@st.cache
def load_data(movie_name):
    return movie_data(movie_name)


@st.cache(allow_output_mutation=True)
def geo_data(locations_df):
    locations_df = enrich_locations(locations_df)
    return locations_df

st.title('Movie Scene Set Locations')

def app():

    if path.exists('movie.json'):
        movie_name = json.load(open('movie.json', 'r'))['movie']
        #st.write(movie_name)

    if movie_name:
        #get data
        movie_meta, quotes_df, reviews_df, locations_df = load_data(movie_name)

        st.header ("All Locations By Country")
        locations_df = geo_data(locations_df)
        country_list = list(locations_df['country'].unique())
        map_dict = {}
        for country in country_list:
            map_dict[country] = plot_location_map(locations_df, country)


        for country in map_dict:
            st.subheader(country)
            show_map = folium_static(map_dict[country])
            st.markdown(
                "<iframe title={} src= {} width='240' height='180' frameBorder='0' allowFullScreen></iframe>".format(country ,show_map),
                unsafe_allow_html=True)
