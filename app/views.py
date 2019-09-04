from app import app
from flask import render_template, request, redirect, url_for, flash

import configparser, requests, json

#para la llamada a la API
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['DEFAULT']['API_KEY']
movie_search = config['DEFAULT']['movie_search']
detail_search = config['DEFAULT']['detail_search']


@app.route ('/')
def index():
    return render_template('index.html')

@app.route ('/films', methods=['GET'])
def busqueda():
    if request.method == 'GET':
        busqueda = request.values.get('busqueda')
        print (busqueda)
        movies = llamadaAPI (busqueda)
        return render_template('films.html', movies=movies, busqueda=busqueda)


@app.route ('/film', methods=['GET'])
def detalle():
    if request.method == 'GET':
        id = request.values.get(request.values.get('ix'))
        movieDetail = llamadaAPIdetail(id)
        busquedaAnterior = request.values.get('busquedaAnterior')
    return render_template('film.html', movieDetail=movieDetail, busquedaAnterior = busquedaAnterior)
    

#Llama a la API por búsqueda
def llamadaAPI(busqueda, pag='1'):
    url = movie_search.format(API_KEY, busqueda, pag)
    response = requests.get(url)

    if response.status_code == 200:
        movies = json.loads(response.text)
        return movies
    else:
        print('Se ha producido un error en la petición: ', response.status_code)

#Llama a la API por id
def llamadaAPIdetail(id):
    url = detail_search.format(API_KEY, id)
    response = requests.get(url)

    if response.status_code == 200:
        detail = json.loads(response.text)
        print(detail)
        return detail
    else:
        print('Se ha producido un error en la petición: ', response.status_code)

    






