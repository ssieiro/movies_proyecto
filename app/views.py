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
        #valida si venimos de index (por búsqueda) o de films (por los botones anterior o siguiente)
        if request.values.get('paginaAnterior') or request.values.get('paginaSiguiente'):
            if request.values.get('paginaAnterior'):
                pag = int(request.values.get('paginaAnterior')) -1
            if request.values.get('paginaSiguiente'):
                pag = int(request.values.get('paginaSiguiente')) +1
            movies, pagActual = llamadaAPI (busqueda, pag) #envía la página actual y la búsqueda
        else:
            try:
                pag = int(request.values.get('pagActual'))
                movies, pagActual = llamadaAPI (busqueda, pag) #envía solo búsqueda porque pag es 1
            except ErrorBusqueda as e:
                mensajeError = str(e)
                return render_template('index.html', error=mensajeError)      
        pagActual = int(pagActual)
        totalResults = int(movies['totalResults'])

        if totalResults % 10 != 0: # calcula el número de páginas en función del total de resultados
            numPags = totalResults // 10 + 1
        else:
            numPags = totalResults // 10
        numResultados = len(movies['Search']) #envía el número de resultados para maquetar (si es la última pag puede ser distinto de 10)
        return render_template('films.html', movies=movies, busqueda=busqueda, numPags=numPags, pagActual=pagActual, numResultados=numResultados)


@app.route ('/film', methods=['GET'])
def detalle():
    if request.method == 'GET':
        pagActual = pag = int(request.values.get('pagActual'))
        id = request.values.get(request.values.get('ix'))
        movieDetail = llamadaAPIdetail(id)
        busquedaAnterior = request.values.get('busquedaAnterior')
    return render_template('film.html', movieDetail=movieDetail, busquedaAnterior = busquedaAnterior, pagActual=pagActual)
    
class ErrorBusqueda(Exception):
    pass


#Llama a la API por búsqueda y nos devuelve el json y la página actual de búsqueda
def llamadaAPI(busqueda, pag='1'):
    if busqueda == '': #si la busqueda está vacía lanza una excepción
        raise ErrorBusqueda("Por favor, introduzca el nombre de una película")
    url = movie_search.format(API_KEY, busqueda, pag)
    response = requests.get(url)


    if response.status_code == 200:
        movies = json.loads(response.text)
        if movies['Response'] == 'True':
            return movies, pag
        else:
            raise ErrorBusqueda("Tu búsqueda no ha obtenido resultados, prueba con otro título") #si la búsqueda no da ningún resultado lanza una excepción

#Llama a la API por id
def llamadaAPIdetail(id):
    url = detail_search.format(API_KEY, id)
    response = requests.get(url)

    if response.status_code == 200:
        detail = json.loads(response.text)
        return detail
    else:
        print('Se ha producido un error en la petición: ', response.status_code)

    






