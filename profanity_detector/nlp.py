from get_data import movie_data

movie_meta, quotes_df, reviews_df, locations_df = movie_data('matrix')
print(reviews_df)
