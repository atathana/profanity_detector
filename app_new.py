import streamlit as st
from multiapp import MultiApp
from apps import home, sentiment, spotify  # import your app modules here
from PIL import Image
import numpy as np

app = MultiApp()

# Title of the main page

st.title("I m BD - International Movie Bible Application ")


# Add all your application here
app.add_app("Home", home.app)
app.add_app("Sentiment", sentiment.app)
app.add_app("Spotify", spotify.app)
# The main app
app.run()
