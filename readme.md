# Instalar dependecias

>pip install -r requirements.txt

# Lanzar aplicación

Crear variable de entorno 

>FLASK_APP=run.py

# Lanzar aplicación en desarrollo

> flask run

#Obtener API KEY

http://www.omdbapi.com/apikey.aspx

#Crear config.ini con nuestra API_KEY y la llamada

[DEFAULT]

API_KEY=[yourkey]
movie_search=http://www.omdbapi.com/?apikey={}&s={}&{}

