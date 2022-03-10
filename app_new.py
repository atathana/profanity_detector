import streamlit as st
from multiapp import MultiApp
from apps import home, sentiment, spotify,locations  # import your app modules here


app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Sentiment", sentiment.app)
app.add_app("Spotify", spotify.app)
app.add_app("Locations", locations.app)

# The main app
app.run()
