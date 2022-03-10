from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from profanity_detector.get_data import movie_data
from profanity_detector.geo_data import geo_map_main
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud
from profanity_detector.nlp import vader_percent_analysis,most_hateful,most_offensive,hate_speech_classifier,vader_sentiment_analysis
from profanity_detector.movie_features import create_word_cloud, plot_word_cloud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greetings": "Hello world"}

@app.get("/display_movie_data")
def display_movie_data(movie_name):
    meta, quotes, reviews, locations = movie_data(movie_name)
    display_reviews = reviews.to_json()
    results =  {"meta": meta,
                "quotes":quotes,
                "locations": locations,
                "reviews" : display_reviews}
    return results

@app.get("/display_sentiment")
def display_sentiment(movie_name):
    meta, quotes_df, reviews_df, locations_df = movie_data(movie_name)
    hate_quote = most_hateful(hate_speech_classifier(quotes_df))
    offensive_quote = most_offensive(hate_speech_classifier(quotes_df))
    hate_review = most_hateful(hate_speech_classifier(reviews_df))
    offensive_review = most_offensive(hate_speech_classifier(reviews_df))
    vader_analysis_reviews = vader_percent_analysis(vader_sentiment_analysis(reviews_df))
    vader_analysis_quotes = vader_percent_analysis(vader_sentiment_analysis(quotes_df))
    categ_quotes = hate_speech_classifier(quotes_df)
    data = {"Hate Speech":categ_quotes.Class.value_counts()[-1], 
            "Offensive Speech": categ_quotes.Class.value_counts()[1], 
            "Neither":categ_quotes.Class.value_counts()[0]}
    
    return{
        "most_hateful_quote":hate_quote,
        "most_offensive_quote": offensive_quote,
        "hate_review": hate_review,
        "offensive_review": offensive_review,
        "sentiment_reviews": vader_analysis_reviews,
        "sentiment_quotes": vader_analysis_quotes,
        "categ_quotes":categ_quotes
        }
#@app.get("/word_cloud")
#def word_cloud(movie_name):
    #meta, quotes, reviews, locations = movie_data(movie_name)
    #word_cloud_quotes = create_word_cloud(quotes,meta['characters'])
    #temp_word = word_cloud_quotes.to_json()
    #return {"word_cloud": temp_word}