# Instalar dependencias

>pip install -r requirements.txt

# Obtener API KEY

http://www.omdbapi.com/apikey.aspx

# Crear config.ini con nuestra API_KEY y la llamada

```
[DEFAULT]

API_KEY=[YOUR KEY]
movie_search=http://www.omdbapi.com/?apikey={}&s={}&page={}
movie_search_type=http://www.omdbapi.com/?apikey={}&s={}&type={}&page={}
detail_search=http://www.omdbapi.com/?apikey={}&i={}
```
# Lanzar aplicación

Crear variable de entorno 

>export FLASK_APP=run.py

# Lanzar aplicación en desarrollo

> flask run
