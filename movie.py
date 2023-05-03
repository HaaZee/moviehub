import tmdbsimple as tmdb
from pprint import pprint
import re

tmdb.API_KEY = os.environ['tmdb_api']

def get_info(id):
    movie = tmdb.Movies(id)
    response = movie.info()

    image = "https://image.tmdb.org/t/p/w342/{}".format(movie.poster_path)
    title = movie.title
    tagline = movie.tagline
    vote_average = movie.vote_average
    release_year = movie.release_date[0:4]
    runtime = movie.runtime
    langauge = movie.original_language

    genres = movie.genres
    genre_list = []
    for d in genres:
        for k, v in d.items():
            try:
                if v.isalpha:
                    genre_list.append(v)
            except AttributeError:
                pass

    overview = movie.overview
    homepage = movie.homepage
    imdb = "https://www.imdb.com/title/{}".format(movie.imdb_id)
    id = movie.id

    data = []
    data.extend((image, title, tagline, vote_average, release_year, str(runtime), langauge, overview, homepage, imdb, id))
    return data, genre_list

def search_by_name(movie):
    search = tmdb.Search()
    res = search.movie(query=movie)
    return res

def search_by_id(id):
    data = get_info(id)

    return data

def get_recent():
    res = tmdb.Movies().popular()['results']
    return res
