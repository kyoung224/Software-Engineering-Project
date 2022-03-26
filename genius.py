import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

AccessToken = os.getenv("GeniusAccessToken")

BASE_URL = "http://api.genius.com/search"

def get_lyrics(title):

    # parameters needed to fetch informations from api
    # variable title is passed from app.py to correspond it with the random artist generated
    params = {
        "q": title,
        "access_token": AccessToken,
    }

    # api json 
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # fetching link to lyrics corresponding with title
    lyrics = data["response"]["hits"][0]["result"]["url"]

    # store variable to be able to reference back in app.py
    return {
        "lyrics": lyrics,
    }