# Crear una instancia de FastAPI y las librerias

from fastapi import FastAPI
import pandas as pd
from datetime import datetime
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity 

#Cargamos los archivos necesarios 

df_games_money = pd.read_csv("df_games_moneyv1.csv", sep=',', encoding='utf-8-sig')
df_games_top = pd.read_csv("df_games_topv1.csv", sep=',', encoding='utf-8-sig')
df_games_ano = pd.read_csv("df_games_anov1.csv", sep=',', encoding='utf-8-sig')
df_games_sentiment = pd.read_csv("df_games_sentimentv1.csv", sep=',', encoding='utf-8-sig')
df_reviews_ano = pd.read_csv("df_reviews_anov1.csv", sep=',', encoding='utf-8-sig')
df_reviews_sentiment = pd.read_csv("df_reviews_sentimentv1.csv", sep=',', encoding='utf-8-sig')
df_items_money = pd.read_csv("df_items_moneyv1.csv", sep=',', encoding='utf-8-sig')
df_items_time = pd.read_csv("df_items_timev1.csv", sep=',', encoding='utf-8-sig')
df_items_top = pd.read_csv("df_items_topv1.csv", sep=',', encoding='utf-8-sig')


app = FastAPI()
#1
#  muestra la cantidad de dinero gastado por el usuario, el porcentaje de recomendación basándonos en reviews.recommend 
# y cantidad de ítems

@app.get('/userdata/')

def userdata(User_id: str):
    # Se obtiene una lista de los IDs 
    item_ids = df_items_money[df_items_money['user_id_items'] == User_id]['item_id'].tolist()
    
    # Se obtiene la cantidad de elementos 
    items_count = len(item_ids)
    
    # Se inicia la suma del dinero gastado en 0
    total_money_spent = 0

    # Se itera a través de los IDs 
    for item_id in item_ids:
        # Se obtiene la suma del precio de los juegos comprados por el usuario
        item_price_sum = df_games_money[df_games_money['id'] == item_id]['price'].sum()
        total_money_spent += item_price_sum
    
    # Se calcula el porcentaje de recomendación (basado en reseñas positivas)
    recommend_true_count = df_reviews_ano[(df_reviews_ano['user_id_reviews'] == User_id) & (df_reviews_ano['recommend'] == True)].shape[0]
    total_reviews_count = df_reviews_ano[df_reviews_ano['user_id_reviews'] == User_id].shape[0]
    
    if total_reviews_count > 0:
        recommend_percentage = (recommend_true_count / total_reviews_count) * 100
    else:
        recommend_percentage = 0
    
    # Se devuelve un diccionario con los resultados
    return {
        "money_spent": total_money_spent,  # Dinero total gastado por el usuario
        "recommend_percentage": recommend_percentage,  # Porcentaje de recomendación basado en reseñas positivas
        "items_count": items_count  # Cantidad de elementos comprados por el usuario
    }
    

#2  muestra Cantidad de usuarios que realizaron reviews entre las fechas dadas y, el porcentaje de recomendación de los mismos 
#  con base en reviews.recommend.

@app.get('/countreviews/')

def countreviews(start_date: str, end_date: str):
    # Se convierte las fechas a datetime
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

    # Se Convierte la columna 'posted' en datetime
    df_reviews_ano['posted'] = pd.to_datetime(df_reviews_ano['posted'], errors='coerce')

    # Se filtra las reseñas en  fechas
    filtered_reviews = df_reviews_ano[(df_reviews_ano['posted'] >= start_datetime) & (df_reviews_ano['posted'] <= end_datetime)]

    # Se cuenta la cantidad de usuarios únicos que realizaron reseñas en ese rango de fechas
    unique_users_count = len(filtered_reviews['user_id_reviews'].unique())

    # Se calcula el porcentaje de recomendación basado en la columna 'recommend'
    recommend_true_count = filtered_reviews[filtered_reviews['recommend'] == True].shape[0]
    total_reviews_count = filtered_reviews.shape[0]

    if total_reviews_count > 0:
        recommend_percentage = (recommend_true_count / total_reviews_count) * 100
    else:
        recommend_percentage = 0


    # Se da como resultado un diccionario 
    return {
        "unique_users_count": unique_users_count,  # Cantidad de usuarios únicos que realizaron reseñas en el rango de fechas
        "recommend_percentage": recommend_percentage  # Porcentaje de recomendación 
    }
    

#3  muestra el puesto en el que se encuentra un género sobre el ranking de los mismos analizado bajo la columna PlayTimeForever.

@app.get('/genre/') 
     
def genre(genero: str):
    # Se Filtra para obtener las filas que contienen el género en la lista de géneros.
    genero_df = df_games_top[df_games_top['genres'].apply(lambda x: genero in x if isinstance(x, list) else False)]

    if genero_df.empty:
        return None

    # Se Filtra para obtener solo las filas con item_id presentes en genero_df['id'].
    genero_df = genero_df.merge(df_items_time, left_on='id', right_on='item_id', how='inner')

    # Se Ordena de manera descendente.
    genero_df = genero_df.sort_values(by='playtime_forever', ascending=False)

    # Se busca el índice del DataFrame.
    genero_df = genero_df.reset_index(drop=True)

    # Se obtiene el índice del género buscado.
    index = genero_df.index[0] if not genero_df.empty else None

    # Se suma 1 al índice para obtener el puesto en el ranking (considerando que comienza desde 1).
    if index is not None:
        return index + 1
    else:
        return None


#4 muestra Top 5 de usuarios con más horas de juego en el género dado, con su URL (del user) y user_id.

@app.get('/userforgenre/')

def userforgenre(genre: str):
    # Se Filtra los juegos del genero
    genre_games = df_games_top[df_games_top['genres'].str.contains(genre, case=False, na=False)]
    
    # Se une los DataFrames 
    merged_data = pd.merge(df_items_top, genre_games, left_on='item_id', right_on='id', how='inner')
        
    # Se agrupan por usuarios y  se suman las horas de juego totales
    user_playtime = merged_data.groupby('user_id_items')['playtime_forever'].sum()
    
    # Se obtiene el top 5 de usuarios con más horas de juego
    top_users = user_playtime.nlargest(5)
    
    # Se obtiene información de los usuarios
    top_users_data = merged_data[merged_data['user_id_items'].isin(top_users.index)]
    top_users_data = top_users_data.drop_duplicates(subset='user_id_items')
    
    # Se Crea una lista de diccionarios con la información requerida
    user_info_list = []
    for index, row in top_users_data.iterrows():
        user_info_list.append({
            "user_id_items": row['user_id_items'],
            "user_url": row['user_url'],
            "playtime": row['playtime_forever']
        })
        
     # Se devuelve una lista de diccionarios con los resultados
    return user_info_list

#5 Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren 
#  categorizados con un análisis de sentimiento.

@app.get('/developer/')

def developer(desarrollador: str):
    # Se Filtra columna para el desarrolador
    df_developer = df_games_ano[df_games_ano['developer'] == desarrollador].copy()

    # Se Convierte la columna 'release_date' a tipo datetime
    df_developer['release_date'] = pd.to_datetime(df_developer['release_date'])

    # Se Crea una nueva columna 'year' para el año de lanzamiento
    df_developer['year'] = df_developer['release_date'].dt.year

    # Se Filtra las filas con contenido gratuito
    df_free = df_developer[df_developer['price'] == '0']

    # Se Calcula la cantidad total de elementos y el porcentaje 'año'
    result = df_developer.groupby('year').agg(
        total_items=pd.NamedAgg(column='developer', aggfunc='count'),
        total_free_items=pd.NamedAgg(column='price', aggfunc='count')
    ).reset_index()

    # Se Calcula el porcentaje de contenido gratuito
    result['Free Percentage'] = (result['total_free_items'] / result['total_items']) * 100
    
    # Se da como resultado un diccionario
    response = result.to_dict(orient='records')
    return response

#6 Crear una función que muestre:Si es un sistema de recomendación user-item: recibir una lista con 5 juegos recomendados 
# para dicho usuario

@app.get('/sentiment_analysis/')

def sentiment_analysis(ano: int):

    # Se filtra las reseñas según el año de lanzamiento
    df_games_sentiment['release_date'] = pd.to_datetime(df_games_sentiment['release_date'])
    # Se Filtra usando .loc
    relevant_games = df_games_sentiment[df_games_sentiment['release_date'].dt.year == ano]
    
    relevant_reviews = df_reviews_sentiment[df_reviews_sentiment['item_id'].isin(relevant_games['id'])]

    # Se cuenta la cantidad de registros de reseñas 
    sentiment_counts = relevant_reviews['sentiment_analysis'].value_counts()

    # Se crea y retornar el diccionario de resultados
    result = {
        'Negative': int(sentiment_counts.get(1, 0)),
        'Neutral': int(sentiment_counts.get(0, 0)),
        'Positive': int(sentiment_counts.get(2, 0))
    }
    
    #Se da como resultado un diccionario
    return JSONResponse(content=result)

#7 Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.
# ( se realizo una muestra aleatoria, por redimiento computacional)



@app.get('/user_item/')


def recomendacion_usuario(id_usuario): #tipo de dato?
    df_games_api = pd.read_csv("df_games_apiv1.csv", sep=',', encoding='utf-8-sig')

    #Se crea una matriz de Usuario item
    user_item_matrix = df_games_api.pivot_table(index='user_id_reviews', columns='item_name', values='sentiment_analysis', fill_value=0)

    
    #Se calcula la similitud entre usuarios
    user_similarity = cosine_similarity(user_item_matrix)
    
    # Halla el índice del usuario en la matriz
    index = user_item_matrix.index.get_loc(id_usuario)
    
    # Se calcula la similitud del usuario con todos los demás usuarios
    user_similarities = user_similarity[index]
    
    # Se ordena los usuarios similares en orden descendente a la similitud
    similar_users_indices = user_similarities.argsort()[::-1]
    
    # Encuentra los ítems que el usuario no ha valorado
    items_not_rated_by_user = user_item_matrix.loc[id_usuario] == 0
    recommended_items = user_item_matrix.columns[items_not_rated_by_user]
    
    # Almacena las recomendaciones de los ítems valorados por los usuarios similares
    recommendations = []
    for user_idx in similar_users_indices:
        similar_user_id = user_item_matrix.index[user_idx]
        rated_items = user_item_matrix.loc[similar_user_id]
        top_items = rated_items.index  # Recomienda todos los ítems valorados por usuarios similares
        recommendations.extend(top_items)
        
        # Se limita la cantidad de recomendaciones
        if len(recommendations) >= 5:
            break
    
    return recommendations[:5]  # Devuelve las primeras 5 recomendaciones


#prueba
@app.get('/ping/') 
     
def genre() -> str:
    return "pong"