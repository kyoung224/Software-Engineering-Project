import requests
import base64
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

AUTH_URL = "https://accounts.spotify.com/api/token"

# Authentication
ClientID = os.getenv("SpotifyClientID")
ClientSecret = os.getenv("SpotifyClientSecret")
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': ClientID,
    'client_secret': ClientSecret,
})

auth_response_data = auth_response.json()
access_token = auth_response_data["access_token"]

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

def search_artist(artist_input):

    if artist_input == None or artist_input == "":
        return "-1"
    else:  
        SEARCH_URL = "https://api.spotify.com/v1/search"

        params = {
            'q': artist_input,
            'type': 'artist'
        }

        search_response = requests.get(SEARCH_URL, headers = headers, params = params)
        search_response = search_response.json()

        search_data = search_response["artists"]["items"][0]
        
        def search_artist_ID(search_data):
            # print("Input: ", artist_input)
            # print("Found: ", search_data["name"])
            if search_data["name"] == artist_input:
                return search_data["id"]
            else:
                return "-1"
        
        artistID = search_artist_ID(search_data)

        return {
            'artistID': artistID,
            'artistName': search_data["name"],
        }

def get_data(artistID):

    # fetch artistID loaded from app.py to randomly select artist
    id = artistID
    
    # api used for basic requirements and another api used for extra information 
    BASE_URL =  f"https://api.spotify.com/v1/artists/{id}/top-tracks"
    EXTRA_URL = f"https://api.spotify.com/v1/artists/{id}"

    # parameter needed to fetch informations from api for top tracks
    params = {
    'market': 'US'
    }

    # basic api json 
    response = requests.get(BASE_URL, headers = headers, params = params)
    response = response.json()
    # extra api json
    extra_response = requests.get(EXTRA_URL, headers = headers)
    extra_response = extra_response.json()
    
    # repeated data used in basic api that will be called in other functions
    data = response["tracks"][0]

    def get_song_title(data):
        return data["name"]

    def get_artist(data):
        return data["artists"][0]["name"]

    def get_image(data):
        return data["album"]["images"][0]["url"]
    
    def get_url(data):
        return data["preview_url"]

    # extra features I included to make the web page become more stylish
    def get_spotify_url(data):
        return data["external_urls"]["spotify"]

    def get_album_name(data):
        return data["album"]["name"];
    
    def get_release_date(data):
        return data["album"]["release_date"];
    
    def get_popularity(data):
        return data["popularity"];
    
    def get_track_number(data):
        return data["track_number"];
    
    def get_artist_img(extra_response):
        return extra_response["images"][0]["url"];

    def get_artist_follower(extra_response):
        return extra_response["followers"]["total"];

    def get_artist_genre(extra_response):
        return extra_response["genres"][0];

    def get_artist_page(extra_response):
        return extra_response["external_urls"]["spotify"];

    # store each returned values from the functions to corresponding variables
    title = get_song_title(data)
    artist = get_artist(data)
    image = get_image(data)
    url = get_url(data)
    spotify_url = get_spotify_url(data)
    album_name = get_album_name(data)
    release_date = get_release_date(data)
    popularity = get_popularity(data)
    track_number = get_track_number(data)
    artist_img = get_artist_img(extra_response)
    artist_follower = get_artist_follower(extra_response)
    artist_genre = get_artist_genre(extra_response)
    artist_page = get_artist_page(extra_response)

    # store each variables to be able to reference back in app.py
    return {
        'title': title,
        'artist': artist,
        'image': image,
        'url': url,
        'spotify_url': spotify_url,
        'album_name': album_name,
        'release_date': release_date,
        'popularity': popularity,
        'track_number': track_number,
        'artist_img': artist_img,
        'artist_follower': artist_follower,
        'artist_genre': artist_genre,
        'artist_page': artist_page,
    }
