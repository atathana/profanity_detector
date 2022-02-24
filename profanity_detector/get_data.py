import pandas as pd
from imdb import Cinemagoer


"""
get all movie data (meta + text + locations) in a single object
"""
def get_all_movie_data(movie_name):
    ia = Cinemagoer()
    movie_search = ia.search_movie(movie_name)
    movie_id = movie_search[0].movieID
    movie_data = ia.get_movie(movie_id)
    ia.update(movie_data,'quotes')
    ia.update(movie_data,'reviews')
    ia.update(movie_data,'locations')
    
    
    return movie_data

"""
create meta_data dict
"""
def get_meta_data(movie_data):
    
    # preprocess directors in case of list
    directors = []
    directors_obj = movie_data['director']
    for director in directors_obj:
        directors.append(director['name'])

    # preprocess cast list only keep top 5 listed
    cast = []
    cast_obj = movie_data['cast']
    for actor in cast_obj:
        cast.append(actor['name'])

    cast = cast[:5]

    # collect all data points to dict
    movie_meta = { "imdb_id": movie_data['imdbID'],
                   "title": movie_data['title'],
                   "rating": movie_data['rating'],
                   "director": directors,
                   "runtime" : '{0} Min'.format(movie_data['runtimes'][0]),
                   "genres" : movie_data['genres'],
                   "year" : movie_data['year'],
                   "box_office" : movie_data['box office']['Cumulative Worldwide Gross'],
                   "top_250_rank" : movie_data['top 250 rank'],
                   "cast" : cast, 
                   "cover_url" : movie_data['cover url'],
                   "akas" : movie_data['akas'],
                   "countries" : movie_data['countries']
                 }
    return movie_meta

"""
create quote df
"""
def get_movie_quotes_df(movie_data):
    #create quotes dict
    quotes_dict = {"imdb_id": movie_data['imdbID'],
                   "title": movie_data['title'],
                   "quotes": movie_data['quotes']}
    #create quotes df
    quotes_df = pd.DataFrame(quotes_dict)
    #turn quotes from lists to strings
    quotes_df['quotes'] = quotes_df.apply(lambda x : ", ".join(x['quotes']), axis=1)
    quotes_df = quotes_df.rename(columns={"quotes": "content"})

    return quotes_df


"""
create reviews df
"""
def get_movie_reviews_df(movie_data):
    #create quotes df
    reviews_df = pd.DataFrame(movie_data['reviews'])
    reviews_df['imdb_id'] = movie_data['imdbID']
    reviews_df['title'] = movie_data['title']
      
    return reviews_df


"""
create filming locations df
"""
def get_movie_locations_df(movie_data):
    #create quotes df
    locations_df = pd.DataFrame(movie_data['locations'])
    locations_df['imdb_id'] = movie_data['imdbID']
    locations_df['title'] = movie_data['title']
    locations_df = locations_df.rename(columns={0: "locations"}) 
    return locations_df

"""
main function
"""
def movie_data(movie_name):

    movie_data = get_all_movie_data(movie_name)
    movie_meta = get_meta_data(movie_data)
    quotes_df = get_movie_quotes_df(movie_data)
    reviews_df = get_movie_reviews_df(movie_data) 
    locations_df = get_movie_locations_df(movie_data)

    return movie_meta, quotes_df, reviews_df, locations_df



if __name__ == '__main__':

    movie_name = input("What Is Your Favourite Movie? : ")
    movie_meta, quotes_df, reviews_df, locations_df = movie_data(movie_name)
    print('Movie Details: \n', movie_meta)
    print('\n')
    print('First 5 Quotes: \n',quotes_df.head())
    print('\n')
    print('First 5 Reviews: \n', reviews_df.head())
    print('\n')
    print('First 5 Locations: \n',locations_df.head())