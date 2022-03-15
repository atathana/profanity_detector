import os
import requests
import datetime
from urllib.parse import urlencode
import base64
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from dotenv import load_dotenv

# Loading API_keys
load_dotenv()
if 'client_id' in os.environ:
    client_id = os.getenv('client_id')
else:
    client_id = os.environ['client_id']

if 'client_secret' in os.environ:
    client_secret = os.getenv('client_secret')
else:
    client_secret = os.environ['client_secret']

#class+search method
#another search method type https://developer.spotify.com/documentation/web-api/reference/#/operations/search


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expires = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)  #inherit from another class
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        return 64 string
        """

        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("you must set client id and client secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization":
            f"Basic {client_creds_b64}"  #Basic <base64 encoded client_id:client_secret>"
        }

    def get_token_data(self):
        return {"grant_type": 'client_credentials'}

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()

        r = requests.post(token_url, data=token_data, headers=token_headers)

        if r.status_code not in range(200, 299):
            raise Exception("Not authenticate client")
        token_response_data = r.json()
        now = datetime.datetime.now()
        data = r.json()

        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):

        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()

        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token

        return token

    #header
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    #depending on input data, get Json
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    #research Json
    def base_search(self, query_params):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    #query : dic or string  %20 is space
    def search(self,
               query=None,
               operator=None,
               operator_query=None,
               search_type='track'):
        if query == None:
            raise Exception("A query is required")

        if isinstance(query, dict):
            query = " ".join(
                [f"{key},{value}" for key, value in query.items()])  #inline

        if operator != None and operator_query != None:
            operator = operator.upper()
            if operator == "or" or operator.lower == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query}{operator}{operator_query}"

        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

        #playlist_json_data
    def playlist_search_json_createdata(self, query="tatanic"):
        playlists_json = self.search(query=query, search_type="playlist")

        #Data
        need_playlist = []
        for i, item in enumerate(playlists_json["playlists"]["items"]):
            need_playlist.append((
                i,
                item["name"],
                item["external_urls"]["spotify"],
                item["id"],
                item["images"][0]["url"],
            ))
            playlist_df = pd.DataFrame(need_playlist,
                                       index=None,
                                       columns=('item', 'Name', 'PlaylistURL',
                                                'ID', 'ImageURL'))
        return playlist_df

    def get_track_from_playlist(self, playlist_link):
        #use the clint secret and id details
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret)
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]

        track_uri_lis = []
        for track in sp.playlist_tracks(playlist_URI)["items"]:
            #URI
            track_uri = track["track"]["uri"]

            #id
            track_id = track["track"]["id"]

            #Track name
            track_name = track["track"]["name"]
            popularity = track["track"]["popularity"]

            #Main Artist
            artist_uri = track["track"]["artists"][0]["uri"]
            artist_info = sp.artist(artist_uri)

            #Album
            album = track["track"]["album"]["name"]

            #energy
            energy = sp.audio_features(track_uri)[0]["energy"]

            all_lis = [
                album, track_name, popularity, energy, track_uri, track_id
            ]
            track_uri_lis.append((all_lis))

            Track_df = pd.DataFrame(track_uri_lis,
                                    index=None,
                                    columns=('album', 'track_name',
                                             "popularity", "energy",
                                             'track_uri', "id"))
            Sort_DF = Track_df.sort_values(by=['popularity'], ascending=False)

        return Sort_DF
