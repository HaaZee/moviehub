import requests
import os

headers = {
    'accept': 'application/json',
    'ApiKey': os.environ['tmdb_api'],
    'Content-Type': 'application/json',
}

data = '{ "theMovieDbId": 299537, "languageCode": "string"}'

response = requests.post('http://localhost:3579/api/v1/Request/movie', headers=headers, data=data)
