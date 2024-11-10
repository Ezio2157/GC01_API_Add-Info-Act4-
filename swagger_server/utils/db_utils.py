import sqlite3

def get_db_connection():
    """
    Establece y retorna una conexión con la base de datos SQLite.
    """
    conn = sqlite3.connect('AddInfo.db')
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

def execute_query(query, params=()):
    """
    Ejecuta una consulta que no requiere retorno de resultados.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return {'status': 'success', 'rowcount': cursor.rowcount}
    except sqlite3.Error as e:
        return {'status': 'failed', 'error': str(e)}
    finally:
        conn.close()

def fetch_query(query, params=()):
    """
    Ejecuta una consulta y retorna los resultados.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return {'status': 'success', 'data': results}
    except sqlite3.Error as e:
        return {'status': 'failed', 'error': str(e)}
    finally:
        conn.close()
