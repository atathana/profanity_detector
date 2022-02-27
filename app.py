import streamlit as st
from profanity_detector.giphy import get_giphy
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.get_data import movie_data
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
#from profanity_detector.feature_data_enrichment import get_geolocation_data

#movie_name ='the matrix'

st.title('I m BD')
st.text('International Movie Bible Dashboard')
#get movie name
#movie_name = input("What Is Your Favourite Movie? : ")

movie_name = st.text_input("What Is Your Favourite Movie? : ", '')

if movie_name:

    col1, col2, col3 = st.columns(3)

    #get data
    movie_meta, quotes_df, reviews_df, locations_df = movie_data(movie_name)

    with col1:
        st.header ("Cover")
        #show_cover
        st.image(movie_meta['cover_url'], 
                 use_column_width='auto',
                 caption=movie_meta['title'])

    #show_meta_data
    with col2:
        st.header ("Movie Info")
        st.subheader('Title')
        st.text(movie_meta['title'])
        
        st.subheader('IMDB Rating')
        st.text(movie_meta['rating'])

        st.subheader('Director')
        for director in movie_meta['director']:
            st.text(director)

        st.subheader('Genres')
        with st.expander("See All Related Genres"):
            for genre in movie_meta['genres']:
                st.text(genre)
        
        st.subheader('Year')
        st.text(movie_meta['year'])
        
        st.subheader('Box Office')
        st.text(movie_meta['box_office'])
        
        st.subheader('Top 250 Rank')
        st.text(movie_meta['top_250_rank'])

        st.subheader('Countries')
        with st.expander("See Countries"):
            for country in movie_meta['countries']:
                st.text(country)
        
        st.subheader('Cast')
        with st.expander("See Cast List"):
            for member in movie_meta['cast']:
                st.text(member)
        

    
    with col3:
        st.header ("Gifs")
        #get giphs
        movies = get_giphy(movie_name)
        print(movies)

        for movie in movies:
            st.markdown(
                "<iframe src= {} width='240' height='180' frameBorder='0' class='giphy-embed' allowFullScreen></iframe>".format(movie),
                unsafe_allow_html=True)
