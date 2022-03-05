from profanity_detector.get_data import movie_data
from geopy.geocoders import Nominatim
import geograpy
import pandas as pd

def get_movie_location(location):
    if '::' in location:
        splitlist = location.split('::')
        movie_location = splitlist[1]

    else:
        movie_location = ''

    return movie_location


def get_set_location(location):
    if '::' in location:
        splitlist = location.split('::')
        set_location = splitlist[0]

    else:
        set_location = location


    return set_location



def get_coordinates(location):
    '''
    get coordinates, if immposible - extract city, region, country and get approximate coordinates
    '''
    #request coordinates
    loc = Nominatim(user_agent="profanity_detector")
    getLoc = loc.geocode(location)

    # check if coordinates found, if not normalize location string and get aprox location
    if getLoc is None:

        #instatiate geofrapy
        places = geograpy.get_place_context(text=location)

        #extract country
        country = places.countries[0] if places.countries != [] else ''

        #extract region
        if places.regions != [] and places.regions[0] != places.countries[0]:
            region = places.regions[0]
        elif places.regions != [] and places.regions[0] == places.countries[0] and len(places.regions) > 1:
             region = places.regions[1]
        else:
            region = ''

        #extract city
        city = places.cities[0] if places.cities != [] else ''

        #create alt_location string
        loc_parse = [city, region, country]
        place = []
        for l in loc_parse:
            if l != '':
                place.append(l)
        alt_location = ', '.join(place)

        #get coordinates for alt_location
        getLoc = loc.geocode(alt_location)

    # if still coordinates not found - drop city
    if getLoc is None:
        alt_list = alt_location.split(',')
        alt_list.remove(alt_list[0])
        alt_location = ', '.join(alt_list)
        getLoc = loc.geocode(alt_location)

    latitude = getLoc.latitude
    longitude = getLoc.longitude



    return latitude, longitude


def get_country_from_coordinates(latitude, longitude):
    loc = Nominatim(user_agent="profanity_detector")
    reverse_location = loc.reverse([latitude, longitude])
    country_name = reverse_location.raw['address']['country']
    return country_name




def enrich_locations(locations_df):
    #limit to 25 locations - linit of nominatim seems to be 35
    locations_df = locations_df.iloc[:34,:]

    #split scene names  string from geolocation strings
    locations_df['movie_location'] = locations_df.apply(lambda x: get_movie_location(x['locations']), axis=1 )
    locations_df['set_location'] = locations_df.apply(lambda x: get_set_location(x['locations']), axis=1 )

    #get coordinates
    locations_df[['latitude','longitude']] = locations_df.apply(lambda x: get_coordinates(x['set_location']) , axis=1, result_type='expand')

    #get country name for each location
    locations_df['country'] = locations_df.apply(lambda x: get_country_from_coordinates(x['latitude'], x['longitude']), axis=1)

    return locations_df
