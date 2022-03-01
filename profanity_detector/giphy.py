import os
from dotenv import load_dotenv
import json
from urllib import parse, request

#load_dotenv()
#API_KEY = os.getenv('giphy_KEY')
API_KEY = os.environ["giphy_KEY"]

def get_giphy(movie_name):
    giphy_list = []
    url = "http://api.giphy.com/v1/gifs/search"

    params = parse.urlencode({
        "q": movie_name,  #VARIABLE
        "api_key": API_KEY,
        "limit": "5"
    })
    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read().decode('utf8'))

    for i in range(5):
        giphy_list.append(data['data'][i]['embed_url'])

    return giphy_list


#print(get_giphy('matrix'))
