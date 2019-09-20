from app import app
from flask import render_template, request, redirect, url_for, flash

import configparser, requests, json

#para la llamada a la API
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['DEFAULT']['API_KEY']
movie_search = config['DEFAULT']['movie_search']
movie_search_type = config['DEFAULT']['movie_search_type']
detail_search = config['DEFAULT']['detail_search']


@app.route ('/')
def index():
    return render_template('index.html')

@app.route ('/films', methods=['GET'])
def busqueda():
    if request.method == 'GET':
        searchType = request.values.get('searchType') #Tipo a buscar (todas, series, peliculas, episodios)
        busqueda = request.values.get('busqueda') #palabras a buscar
        pagActual = int(request.values.get('pagActual')) #Página de la búsqueda que queremos que devuelva
        #valida si venimos por los botones anterior o siguiente para añadir o restar 1 a la página
        if request.values.get('paginaAnterior') or request.values.get('paginaSiguiente'):
            if request.values.get('paginaAnterior'):
                pagActual = int(request.values.get('paginaAnterior')) -1
            if request.values.get('paginaSiguiente'):
                pagActual = int(request.values.get('paginaSiguiente')) +1
        #Llama a la función llamadaAPI y, si no funciona, devuelve una excepción y un error
        try:
            movies = llamadaAPI (busqueda, pagActual, searchType)
        except ErrorBusqueda as e:
            mensajeError = str(e)
            return render_template('index.html', error=mensajeError)
        #Calcula el número de páginas que puede haber en función del numero total de resultados para la maquetación
        totalResults = int(movies['totalResults'])
        if totalResults % 10 != 0: 
            numPags = totalResults // 10 + 1
        else:
            numPags = totalResults // 10
        numResultados = len(movies['Search'])
        return render_template('films.html', movies=movies,
                                             busqueda=busqueda,
                                             numPags=numPags,
                                             pagActual=pagActual,
                                             searchType=searchType,
                                             numResultados=numResultados)


@app.route ('/film', methods=['GET'])
def detalle():
    #Llama a la función llamadaAPIdetail enviando el id de la película
    if request.method == 'GET':
        searchType = request.values.get('searchType')
        pagActual = int(request.values.get('pagActual'))
        id = request.values.get(request.values.get('ix'))
        movieDetail = llamadaAPIdetail(id)
        busquedaAnterior = request.values.get('busquedaAnterior')
    return render_template('film.html', movieDetail=movieDetail, busquedaAnterior = busquedaAnterior, pagActual=pagActual, searchType=searchType)


class ErrorBusqueda(Exception):
    pass

#Llama a la API por búsqueda y nos devuelve el json y la página actual de búsqueda
def llamadaAPI(busqueda, pag, searchType):
    if busqueda == '': #si la busqueda está vacía lanza una excepción
        raise ErrorBusqueda("Por favor, introduzca el nombre de una película")
    if searchType == "All":
        url = movie_search.format(API_KEY, busqueda, pag) # Si se selecionan "todas" llama sin el parámetro type
    else:
        url = movie_search_type.format(API_KEY, busqueda, searchType, pag) #Si nos informan del tipo llama enviando el parametro type
        

    response = requests.get(url)

    if response.status_code == 200:
        movies = json.loads(response.text)
        if movies['Response'] == 'True':
            return movies
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

    






