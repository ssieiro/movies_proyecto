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
        #si venimos desde pagina anterior o pagina siguiente aumenta el valor de pag para la búsqueda
        if request.values.get('paginaAnterior') or request.values.get('paginaSiguiente'): 
            if request.values.get('paginaAnterior'):
                pag = int(request.values.get('paginaAnterior')) -1
            if request.values.get('paginaSiguiente'):
                pag = int(request.values.get('paginaSiguiente')) +1
            movies, pagActual = llamadaAPI (busqueda, pag) #envía si la página es distinta el valor pag a la funcion llamadaAPI
        else:
            movies, pagActual = llamadaAPI (busqueda) #Recibe la página actual y el json de la búsqueda
        
        pagActual = int(pagActual)
        totalResults = int(movies['totalResults'])

        if totalResults % 10 != 0: #nos devuelve el número de páginas
            numPags = totalResults // 10 + 1
        else:
            numPags = totalResults // 10
        numResultados = len(movies['Search']) #para que al llegar a la ultima pagina si son 3 resultados en lugar de 10 se maquete en función de eso
        return render_template('films.html', movies=movies, busqueda=busqueda, numPags=numPags, pagActual=pagActual, numResultados=numResultados)


@app.route ('/film', methods=['GET'])
def detalle():
    if request.method == 'GET':
        id = request.values.get(request.values.get('ix'))
        movieDetail = llamadaAPIdetail(id)
        busquedaAnterior = request.values.get('busquedaAnterior')
    return render_template('film.html', movieDetail=movieDetail, busquedaAnterior = busquedaAnterior)
    

#Llama a la API por búsqueda y nos devuelve el json y la página actual de búsqueda
def llamadaAPI(busqueda, pag='1'):
    url = movie_search.format(API_KEY, busqueda, pag)
    response = requests.get(url)

    if response.status_code == 200:
        movies = json.loads(response.text)
        return movies, pag
    else:
        print('Se ha producido un error en la petición: ', response.status_code)

#Llama a la API por id
def llamadaAPIdetail(id):
    url = detail_search.format(API_KEY, id)
    response = requests.get(url)

    if response.status_code == 200:
        detail = json.loads(response.text)
        return detail
    else:
        print('Se ha producido un error en la petición: ', response.status_code)

    






