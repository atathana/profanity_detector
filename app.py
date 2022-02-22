import streamlit as st
from profanity_detector.giphy import get_giphy

movie_name ='titanic'

movies = get_giphy(movie_name)
print(movies)

for movie in movies:
    st.markdown(
        "<iframe src= {} width='480' height='360' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>".format(movie),
        unsafe_allow_html=True)
