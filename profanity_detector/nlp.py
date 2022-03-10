from profanity_detector.get_data import movie_data
from hatesonar import Sonar
import pandas as pd
import warnings
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# HATESONAR

# Instantiate a hatesonar object
def create_sonar_object():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        sonar = Sonar()
    return sonar


# Classify content using Hatersonar package
def hate_speech_classifier(df):

    Class = []
    hate = []
    offensive = []
    neither = []

    # Create an object of Sonar Hate Speech Detection
    sonar = create_sonar_object()

    # Function applying hatesonar on the content column of reviews_df and returning a reviews_df_sonar (incl new info)
    for i in df['content']:
        sonar_dict = sonar.ping(text=i)
        Class.append(list(sonar_dict.values())[1])
        hate.append(list(list(sonar_dict.values())[2][0].values())[1])
        offensive.append(list(list(sonar_dict.values())[2][1].values())[1])
        neither.append(list(list(sonar_dict.values())[2][2].values())[1])

    hatesonar_df = pd.DataFrame({
        "Class": Class,
        "Hate": hate,
        "Offensive": offensive,
        "Neither": neither
    })

    # Updating the reviews dataframe
    df_sonar = pd.concat([df, hatesonar_df], axis=1)

    return df_sonar


def most_hateful(df):

    # sort Hate in an ascending order
    df_sorted = df.sort_values(by='Hate', ascending=False)
    hate_comment = df_sorted.iloc[0]['content']
    #return comment, rate, score
    return hate_comment


def most_offensive(df):

    # sort Hate in an ascending order
    df_sorted = df.sort_values(by='Offensive', ascending=False)
    off_quote = df_sorted.iloc[0]['content']
    return off_quote

# VADER

# instantiate a vader object
def create_vader_object():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        analyzer = SentimentIntensityAnalyzer()
    return analyzer


def vader_sentiment_analysis(df):

    neutral = []
    positive = []
    negative = []
    compound = []

    analyzer = create_vader_object()

    for quote in df['content']:
        sentiment_dict = analyzer.polarity_scores(quote)
        negative.append(sentiment_dict['neg'])
        neutral.append(sentiment_dict['neu'])
        positive.append(sentiment_dict['pos'])
        compound.append(sentiment_dict['compound'])

        vader_df = pd.DataFrame({
            "Negative": negative,
            "Positive": positive,
            "Neutral": neutral,
            "Compound": compound
        })

    # Classifying compound result to pos and neg
    vader_df['Compound'] = vader_df['Compound'].apply(lambda c: 'pos'
                                                      if c >= 0 else 'neg')
    # Updating the reviews dataframe
    df_vader = pd.concat([df, vader_df], axis=1)

    return df_vader


def vader_percent_analysis(df_vader):

    neg_percent = round(
        (df_vader[df_vader['Compound'] == 'neg'].shape[0] / len(df_vader)) *
        100, 1)

    pos_percent = round(
        (df_vader[df_vader['Compound'] == 'pos'].shape[0] / len(df_vader)) *
        100, 1)

    return [pos_percent, neg_percent]


def display_results(reviews_df, quotes_df):

    # Calling Functions to get data

    hate_review = most_hateful(hate_speech_classifier(reviews_df))

    offensive_review = most_offensive(hate_speech_classifier(reviews_df))

    hate_quote = most_hateful(hate_speech_classifier(quotes_df))
    offensive_quote = most_offensive(hate_speech_classifier(quotes_df))

    vader_analysis_reviews = vader_percent_analysis(
        vader_sentiment_analysis(reviews_df))

    vader_analysis_quotes = vader_percent_analysis(
        vader_sentiment_analysis(quotes_df))

    # Display Results:
    print(f""" The review with the highest hated score was:
          {hate_review}
          """)
    print(f"""The most offensive review was:
        {offensive_review}
        """)

    print(f""" The quote with the highest hated score was:
          {hate_quote}
          """)

    print(f"""The most offensive quote was:
          {offensive_quote}
          """)

    print(f""" Sentiment Analysis:
          {movie_meta['title']} has received {vader_analysis_reviews[0]}% positive reviews and {vader_analysis_reviews[1]}% negative.
          A sentiment analysis on quotes has shown that {vader_analysis_quotes[0]}% of are positive and {vader_analysis_quotes[1]}% are negative.
""")


if __name__ == '__main__':
    movie_meta, quotes_df, reviews_df, locations_df = movie_data('lion king')
    display_results(reviews_df, quotes_df)
