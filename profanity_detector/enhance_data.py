from get_data import get_all_movie_data, get_movie_locations_df
from geopy.geocoders import Nominatim

#remove the extra information (e.g. which scene)
def split_location(location):
    return location.split(":")[0]

#the function tries to get the coordinates of the location. In case it
#does note recognize the location, it will take only the last 3 elements
#of the location - usually city, province and country
def get_coordinates(location):
    geolocator = Nominatim(user_agent="profanity_detector")
    film_location = geolocator.geocode(location)
    if film_location is None:
        new_location = location.split(",")[-3:]
        film_location=geolocator.geocode(new_location)
    results = (film_location.latitude, film_location.longitude)
    return results

#apply the geolocation coordinates to the location dataframe
def get_geolocation_data(movie_name):
    #geolocator = Nominatim(user_agent="profanity_detector")
    movie_data = get_all_movie_data(movie_name)
    movie_location = get_movie_locations_df(movie_data)
    movie_location["locations"] = movie_location["locations"].apply(split_location)
    movie_location["latitude"], movie_location["longitude"] = zip(*map(get_coordinates, movie_location["locations"]))
    return movie_location
