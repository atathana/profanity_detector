import json
from os import path
import streamlit as st
import matplotlib.pyplot as plt
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.get_data import movie_data
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.nlp import vader_percent_analysis, most_hateful, most_offensive, hate_speech_classifier, vader_sentiment_analysis
import requests
import pandas as pd

@st.cache
def load_data(movie_name):
    return movie_data(movie_name)


def app():
    st.title('SENTIMENT ANALYSIS')
    st.header(":scroll: Quotes Analysis")

    if path.exists('movie.json'):
        movie_name = json.load(open('movie.json', 'r'))['movie']
        #st.write(movie_name)


        if movie_name:

            col1, col2, col3 = st.columns(3)

            movie_meta, quotes_df, reviews_df, locations_df = load_data(movie_name)
            url = 'https://movie-sentiment-7uhpc5vsza-ez.a.run.app/display_sentiment'
            params = {"movie_name":movie_name}
            response = requests.get(url,params=params).json()
            hate_quote = response["most_hateful_quote"]
            offensive_quote = response["most_offensive_quote"]
            hate_review = response["hate_review"]
            offensive_review = response["offensive_review"]
            vader_analysis_reviews = response["sentiment_reviews"]
            vader_analysis_quotes = response["sentiment_quotes"]
            categ_quotes = pd.DataFrame(response["categ_quotes"])
            data = [categ_quotes.Class.value_counts()[-1], categ_quotes.Class.value_counts()[1], categ_quotes.Class.value_counts()[0]]

            with col1:
                st.subheader('Most Hateful Quote')
                st.markdown(f"_{hate_quote}_")

                st.subheader('Most Offensive Quote')
                st.markdown(f"_{offensive_quote}_") # italic


            with col2:
                st.subheader('Sentiment Quote')
                labels = ['Hate Speech', 'Offensive', 'Neither']
                explode = (0, 0.1, 0.1)
                fig1, ax1 = plt.subplots(nrows=1,
                                         ncols=1,
                                         figsize=(10, 6),
                                         subplot_kw=dict(aspect="equal"),
                                         dpi=80)
                #fig1.patch.set_facecolor(color=None)
                plt.figure(facecolor='black')
                ax1.pie(data,
                        explode=explode,
                        colors=['#e55039', '#3c6382', '#78e08f'],
                        labels=labels,
                        autopct='%1.1f%%',
                        shadow=True,
                        startangle=90)
                ax1.axis(
                    'equal'
                )  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig1)

            with col3:

                st.subheader("QuoteCloud")
                plot_word_cloud(
                    create_word_cloud(quotes_df, movie_meta['characters']))
                st.pyplot()

        st.markdown('---')

        st.header(":memo: Reviews Analysis")


        col4, col5 = st.columns([2,1])
        with col4:

            st.subheader('Most Hateful Review')
            st.markdown(f"_{hate_review}_")

            st.subheader('Most Offensive Review')
            st.markdown(f"_{offensive_review}_")  # italic

        with col5:
            st.subheader("Positive vs Negative Reviews")
            labels_2 = ['Positive', 'Negative']
            data_2 = [vader_analysis_reviews[0], vader_analysis_reviews[1]]
            explode = (0, 0.1)
            fig2, ax2 = plt.subplots(nrows=1,ncols=1)
            plt.figure(facecolor='black')
            ax2.pie(data_2,
                    explode=explode,
                    colors=['#78e08f', '#e55039'],
                    labels=labels_2,
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=90)
            ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig2)

            st.subheader ("ReviewCloud")
            plot_word_cloud(create_word_cloud(reviews_df,movie_meta['characters']))
            st.pyplot()

        st.markdown('---')
