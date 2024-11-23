from swagger_server.utils.db_utils import execute_query, fetch_query

def insert_review(content_id, user_id, profile_id, rating):
    """
    Inserta una nueva reseña en la base de datos.
    """
    query = 'INSERT INTO reviews (content_id, user_id, profile_id, rating) VALUES (?, ?, ?, ?)'
    return execute_query(query, (content_id, user_id, profile_id, rating))

def delete_review(content_id, user_id, profile_id):
    """
    Elimina una reseña de la base de datos.
    """
    query = 'DELETE FROM reviews WHERE content_id = ? AND user_id = ? AND profile_id = ?'
    return execute_query(query, (content_id, user_id, profile_id))

def update_review(content_id, user_id, profile_id, new_rating):
    """
    Actualiza una reseña específica en la base de datos.
    """
    query = 'UPDATE reviews SET rating = ? WHERE content_id = ? AND user_id = ? AND profile_id = ?'
    return execute_query(query, (new_rating, content_id, user_id, profile_id))

def fetch_review(content_id, user_id, profile_id):
    """
    Recupera una reseña específica de la base de datos.
    """
    query = 'SELECT content_id, user_id, profile_id, rating FROM reviews WHERE content_id = ? AND user_id = ? AND profile_id = ?'
    result = fetch_query(query, (content_id, user_id, profile_id))

    if result['status'] == 'success':
        # Convierte cada fila de resultado en un diccionario
        data = [dict(row) for row in result['data']]  # Convierta cada fila en un diccionario
        return {'status': 'success', 'data': data}
    else:
        return result  # Devuelve el resultado tal cual si hay un error

def fetch_reviews_by_user(user_id):
    """
    Recupera todas las reseñas numéricas realizadas por un usuario específico de la base de datos.
    """
    query = 'SELECT content_id, user_id, profile_id, rating FROM reviews WHERE user_id = ?'
    result = fetch_query(query, (user_id,))

    if result['status'] == 'success':
        # Convierte cada fila de resultado en un diccionario
        data = [dict(row) for row in result['data']]
        return {'status': 'success', 'data': data}
    return result  # Devuelve el resultado tal cual si hay un error

def fetch_reviews_for_content(content_id):
    """
    Recupera todas las reseñas numéricas realizadas para un contenido específico de la base de datos.
    """
    query = 'SELECT content_id, user_id, profile_id, rating FROM reviews WHERE content_id = ?'
    result = fetch_query(query, (content_id,))

    if result['status'] == 'success':
        # Convierte cada fila de resultado en un diccionario
        data = [dict(row) for row in result['data']]
        return {'status': 'success', 'data': data}
    return result  # Devuelve el resultado tal cual si hay un error