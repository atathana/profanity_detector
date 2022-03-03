import sys
import os
import requests
import datetime
from  urllib.parse import urlencode
import base64

# client_id = os.environ.get("CLIENTID")
# client_secret=os.environ.get("CLIENTSEC")
client_id ="a2a39f20a23a41fa94057a7e2cb13675"
client_secret="4dc99bfd287e44b8bde2cab06d4b3e05"
#class+search method
#another search method type https://developer.spotify.com/documentation/web-api/reference/#/operations/search


class SpotifyAPI(object):
    access_token=None
    access_token_expires=datetime.datetime.now()
    access_token_did_expires=True
    client_id=None
    client_secret=None    
    token_url='https://accounts.spotify.com/api/token'
    
    def __init__(self,client_id,client_secret,*args,**kwargs):
        super().__init__(*args,**kwargs)#inherit from another class
        self.client_id=client_id
        self.client_secret=client_secret
        
    def get_client_credentials(self):
        """
        return 64 string
        """
        
        client_id=self.client_id
        client_secret=self.client_secret
        if client_secret==None or client_id== None:
            raise Exception("you must set client id and client secret")
        client_creds=f"{client_id}:{client_secret}"
        client_creds_b64=base64.b64encode(client_creds.encode()) 
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64=self.get_client_credentials()
        return {
    "Authorization": f"Basic {client_creds_b64}"#Basic <base64 encoded client_id:client_secret>"
        }
            
    def get_token_data(self):
            return{
    "grant_type": 'client_credentials'
            }
    
    def perform_auth(self):
        token_url=self.token_url
        token_data=self.get_token_data()
        token_headers=self.get_token_headers()
        
        r=requests.post(token_url,data=token_data,headers=token_headers)

        if r.status_code not in range(200,299):
            raise Exception("Not authenticate client")
        token_response_data=r.json()
        now=datetime.datetime.now()
        data=r.json()
        
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
                
        token=self.access_token
        expires=self.access_token_expires
        now=datetime.datetime.now()
        
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token==None:
            self.perform_auth()
            return self.get_access_token
            
        return token
    
    #header
    def get_resource_header(self):
            access_token = self.get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            return headers

    #depending on input data, get Json
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    #album json
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    #artist json 
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    #research Json
    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()
    
    #query : dic or string  %20 is space
    def search(self,query=None, operator=None,operator_query=None ,search_type='track'):
        if query == None:
               raise Exception("A query is required")
               
        if isinstance(query,dict):
               query=" ".join([f"{key},{value}"for key,value in query.items()])#inline 
                
        if operator != None and operator_query!=None:
            operator=operator.upper()
            if operator== "or" or operator.lower=="not":
                operator=operator.upper()
                if isinstance(operator_query,str):
                    query=f"{query}{operator}{operator_query}"
               
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)
    

