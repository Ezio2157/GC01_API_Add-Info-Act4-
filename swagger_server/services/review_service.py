from swagger_server.utils.db_utils import execute_query, fetch_query

def insert_review(content_id, user_id, profile_id, rating):
    """
    Inserta una nueva reseña en la base de datos.
    """
    query = 'INSERT INTO reviews (content_id, user_id, profile_id, rating) VALUES (?, ?, ?, ?)'
    return execute_query(query, (content_id, user_id, profile_id, rating))
