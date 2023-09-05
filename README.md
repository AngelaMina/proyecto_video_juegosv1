# PROYECTO VIDEO JUEGOS    INDIVIDUAL Nº1 -Machine Learning 

Este trabajo se utilizó un dataset dado  dentro del bootcamp de Data Science, como parte del módulo de proyectos prácticos individuales.

Se tiene 3 dataset sobre una página de video juegos, todo los archivos están en formato Json:

1. steam_games consta de 120445 rows × 13 columns donde se relaciona columnas como género, precio, desarrolador 
2. user_reviews consta de 25799 rows × 3 columns donde se relacionan columnas como user_id, url y reviews la cual está anidada
3. user_items consta de 88310 rows × 5 columns donde se relacionan columnas como user_id items_count steam_id e items	

[Dataset juegos](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) 

# Objetivo

El objetivo de este proyecto es tomar la base de datos proporcionada y pasarla por diferentes etapas de limpieza y extracción necesarias para disponibilidad los datos en una API y generar un modelo de recomendación de juegos basado en Machine Learning. 

## Transformaciones

- Desanidar los datos que se encuentran en formato de listas de diccionarios para poder unirlos nuevamente a la base de datos de manera separada.
- Eliminar los registros que contengan valores nulos en la columna 
- Asegurarse de que las columnas "release_date", "posted", "last_edited" esté en formato AAAA-MM-DD 
- Eliminar las columnas innecesarias para el desarrollo de la API

## Desarrollo de la API

- Crear una función que muestre la cantidad de dinero gastado por el usuario, el porcentaje de recomendación basándonos en reviews.recommend y cantidad de ítems
- Crear una función que muestre Cantidad de usuarios que realizaron reviews entre las fechas dadas y, el porcentaje de recomendación de los mismos con base en reviews.recommend.
- Crear una función que muestre el puesto en el que se encuentra un género sobre el ranking de los mismos analizado bajo la columna PlayTimeForever.
- Crear una función que muestre Top 5 de usuarios con más horas de juego en el género dado, con su URL (del user) y user_id.
- Crear una función que Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
- Crear una función que muestre:Si es un sistema de recomendación user-item: recibir una lista con 5 juegos recomendados para dicho usuario

## Desarrollo de EDA

- Explorar los datos limpios para establecer correlaciones entre las variables.

## Sistema de recomendación

- Generar un sistema de recomendación de películas basado en Machine Learning.
- Disponibilidad el sistema de recomendación a través del framework FastAPI.

# Estructura del repositorio

- _ _pycache__: Carpeta donde se almacenan los datos cache de Python para mejorar su proceso de ejecución.
- requirements.txt: Librerías necesarias para la adecuada ejecución de los documentos.
-  main.py: Archivo donde se almacenan las funciones que se ejecutarán en la API.
- eda_and_ml.ipynb Final.ipynb: Documento en formato notebook donde se encuentra el código en el que se desarrolla el EDA y se realizan las transformaciones pertinentes para el desarrollo del sistema de recomendación de juegos.

Los archivos csv para el funcionamiento de la Api

df_games_money.csv
df_games_top.csv
df_games_ano.csv
df_games_sentiment.csv
df_reviews_ano.csv
df_reviews_sentiment.csv
df_items_money.csv
df_items_time.csv
df_items_top.csv
df_games_api.csv

## Limpieza de datos

[Dataset juegos en formato csv](https://drive.google.com/file/d/1YYkvDt1IEMSJbf9ZPtItdvS3ln4dBU7O/view?usp=sharing)  Estos archvos se tienen que descargar junto con el archivo eda_and_ml.ipynb para poder correr las funciones

Durante el proceso de limpieza de datos, se llevaron a cabo las siguientes acciones:
- Se identificaron los valores sin significado para el análisis y se eliminaron.
- Se desanidaron las columnas que contenían valores en formato de listas de diccionarios.
- Se identificaron y eliminaron registros duplicados.
- Se identificaron y eliminaron registros con valores nulos, considerando la relevancia de los nulos por columna.
- Se realizaron identificaciones de outliers, pero no se procedió a su eliminación debido a que estos outliers tienen sentido en el contexto de análisis de los datos.

## Desarrollo del API

Una vez finalizada la limpieza de datos, se descargó la base de datos con las transformaciones realizadas, la cual se utilizó para generar las funciones de consulta que serían empleadas en la API. Dichas funciones se incluyeron en el archivo "main.py" para su uso en la API.

Además, se desarrolló un archivo separado para llevar a cabo el EDA (Exploratory Data Analysis). Durante este análisis se generaron gráficos para explorar las variables y sus relaciones. Posteriormente, se realizó una limpieza adicional en la base de datos, conservando únicamente las variables relevantes para el desarrollo del modelo de recomendación. Debido al tamaño extenso de la base de datos y las limitaciones computacionales, se seleccionó una muestra de 10,000 registros para el desarrollo del modelo.

Una vez se transformaron los datos y se prepararon para alimentar el modelo de recomendación, se descargó la nueva base de datos y se generó una función que utiliza dicha base de datos y el modelo desarrollado utilizando  similitud del coseno. (archivos, mencionados arriba)

## Modelo de recomendación

Se probaron dos algoritmos proporcionados por la librería sklearn para el desarrollo del modelo de recomendación. El primer algoritmo utilizado fue la similitud del coseno, el cual ofreció resultados satisfactorios, para el sistema de recomendación item-item por ID juego Y el segundo también con similitud del coseno el cual también ofreció resultados satisfactorios para el sistema de recomendación user-item por nombre juego; pala implementación de la API se dejó este último.


