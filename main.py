import os
import requests
from flask import Flask, render_template, url_for, flash, redirect, request
from movie import *

app = Flask(__name__)

settings_folder = os.path.join('static', 'settings')

# ROUTES
@app.route('/', methods=['GET', 'POST'])
@app.route('/popular', methods=['GET', 'POST'])
def index():
    movies = get_recent()
    if request.method == "POST":
        movie_name = request.form.get('search_area')
        return redirect(url_for('search', name=movie_name))
    return render_template('home.html', title="MovieHub", movies=movies, heading="Popular Movies")

@app.route('/movie', methods=['GET', 'POST'])
def movie():
    id = request.args.get('id')
    data, genres = search_by_id(id)
    if request.method == "POST":
        movie_name = request.form.get('search_area')
        return redirect(url_for('search', name=movie_name))
    return render_template('movie.html', title="{} - MovieHub -".format(data[1]), data=data, genres=genres)

@app.route("/ombi_request/<id>", methods=['GET', 'POST'])
def ombi_request(id):
    headers = {
        'accept': 'application/json',
        'ApiKey': os.environ['tmdb_api'],
        'Content-Type': 'application/json',
        }
    data = dict()
    data['theMovieDbId'] = id
    data['languageCode'] = 'string'
    data = str(data)

    response = requests.post('http://192.168.1.101:3579/api/v1/Request/movie', headers=headers, data=data)
    if response.json()['result'] == False:
        flash('Movie has already been requested.', 'warning')
    elif response.json()['result'] == True:
        flash('Movie has been requested successfully.', 'success')
    else:
        flash('Unknown error! Movie not requested.', 'danger')

    return redirect(request.referrer)

@app.route('/search/<name>', methods=['GET', 'POST'])
def search(name):
    data = search_by_name(name)
    if request.method == "POST":
        movie_name = request.form.get('search_area')
        return redirect(url_for('search', name=movie_name))
    if data['total_results'] == 1:
        for i in data['results']:
            id = i['id']
        data, genres = search_by_id(id)
        return render_template('movie.html', title="{} - MovieHub -".format(data[1]), data=data, genres=genres, heading=data[1])
    else:
        return render_template('search.html', title="{} - MovieHub -".format(name), movies=data, heading=name)


# UPDATE CSS
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.environ['TOKEN']
    app.run(debug=True, port=os.getenv("PORT", default=5000))
