from swagger_server.utils.db_utils import execute_query, fetch_query

def fetch_view_count(content_id):
    """
    Recupera el número de vistas para un contenido específico de la base de datos.
    """
    query = 'SELECT view_count FROM views WHERE content_id = ?'
    result = fetch_query(query, (content_id,))
    return result

def add_view(content_id, view_count):
    """
    Agrega una nueva entrada de 'views'.
    """
    query = 'INSERT INTO views (content_id, view_count) VALUES (?, ?)'
    result = execute_query(query, (content_id, view_count))
    return result

def update_view(content_id, new_view_count):
    """
    Actualiza la cantidad de 'views' para un contenido.
    """
    query = 'UPDATE views SET view_count = ? WHERE content_id = ?'
    result = execute_query(query, (new_view_count, content_id))
    return result

def delete_view(content_id):
    """
    Elimina una entrada de 'views' para un contenido específico.
    """
    query = 'DELETE FROM views WHERE content_id = ?'
    result = execute_query(query, (content_id,))
    return result
