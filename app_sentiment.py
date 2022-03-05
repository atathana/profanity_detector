import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from profanity_detector.giphy import get_giphy
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.get_data import movie_data
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.nlp import vader_percent_analysis,most_hateful,most_offensive,hate_speech_classifier,vader_sentiment_analysis

st.set_page_config(page_title="I m BD Sentiment",
                   page_icon="film_frames",
                   layout="wide",
                   initial_sidebar_state="expanded")
movie_name = st.text_input("What Is Your Favourite Movie? : ", '')

if movie_name:

    col1, col2 = st.columns(2)

    movie_meta, quotes_df, reviews_df, locations_df = movie_data(movie_name)
    hate_quote = most_hateful(hate_speech_classifier(quotes_df))
    offensive_quote = most_offensive(hate_speech_classifier(quotes_df))
    hate_review = most_hateful(hate_speech_classifier(reviews_df))
    offensive_review = most_offensive(hate_speech_classifier(reviews_df))
    vader_analysis_reviews = vader_percent_analysis(vader_sentiment_analysis(reviews_df))
    vader_analysis_quotes = vader_percent_analysis(vader_sentiment_analysis(quotes_df))
    categ_quotes = hate_speech_classifier(quotes_df)
    data = [categ_quotes.Class.value_counts()[-1], categ_quotes.Class.value_counts()[1], categ_quotes.Class.value_counts()[0]]
    

    with col1:
        st.header("Quotes")
        st.subheader ("QuoteCloud")
        plot_word_cloud(create_word_cloud(quotes_df,movie_meta['characters']))
        st.pyplot()
        st.subheader('Most Hateful Quote')
        st.markdown(hate_quote)
        st.subheader('Most Offensive Quote')
        st.markdown(offensive_quote)
        st.subheader('Sentiment Quote')
        labels = ['Hate Speech', 'Offensive', 'Neither']
        explode = (0, 0.1,0.1) 
        fig1, ax1 = plt.subplots(nrows=1,ncols=1,figsize=(10, 6), subplot_kw=dict(aspect="equal"), dpi= 80)
        ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)


    with col2:
        st.header("Reviews")
        #st.subheader ("ReviewCloud")
        #plot_word_cloud(create_word_cloud(reviews_df,movie_meta['characters']))
        #st.pyplot()
        st.subheader('Most Hateful Review')
        st.markdown(hate_review)
        st.subheader('Most Offensive Review')
        st.markdown(offensive_review)
        #labels2 = ['Hate Speech', 'Offensive', 'Neither']
        # st.header("Sentiment Reviews")
        # explode = (0, 0.1,0.1) 
        # fig2, ax2 = plt.subplots(nrows=1,ncols=1)
        # ax2.pie(data_reviews, explode=explode, labels=labels2, autopct='%1.1f%%',
        # shadow=True, startangle=90)
        # ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # st.pyplot(fig2)


