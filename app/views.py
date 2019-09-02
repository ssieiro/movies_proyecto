from app import app
from flask import render_template, request, redirect, url_for, flash

import configparser, requests, json

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['DEFAULT']['API_KEY']
movie_search = config['DEFAULT']['movie_search']

@app.route ('/')
def index():
    return render_template('index.html')

@app.route ('/films', methods=['GET'])
def busqueda():
    if request.method == 'GET':
        movies = llamadaAPI (request.values.get('busqueda'))
        print(movies)
    return render_template('films.html', movies = movies)
    


@app.route ('/film')
def detalle():
    return render_template('film.html')
    #print (request.values['busqueda'])


def llamadaAPI(busqueda, pag='1'):
    url = movie_search.format(API_KEY, busqueda, pag)
    response = requests.get(url)

    if response.status_code == 200:
        movies = json.loads(response.text)
        return movies
    else:
        print('Se ha producido un error en la petición: ', response.status_code)

    #Llama con un format de la API_KEY, la palabra y el número de página




#print(prueba['Search'][1])

