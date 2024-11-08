from swagger_server.utils.db_utils import execute_query, fetch_query

def fetch_continue_watching(user_id, profile_id, content_id):
    query = 'SELECT last_watched_minute FROM continue_watching WHERE user_id = ? AND profile_id = ? AND content_id = ?'
    return fetch_query(query, (user_id, profile_id, content_id))

def insert_continue_watching(user_id, profile_id, content_id, last_watched_minute):
    query = 'INSERT INTO continue_watching (user_id, profile_id, content_id, last_watched_minute) VALUES (?, ?, ?, ?)'
    return execute_query(query, (user_id, profile_id, content_id, last_watched_minute))

def update_continue_entry(user_id, profile_id, content_id, new_last_watched_minute):
    query = 'UPDATE continue_watching SET last_watched_minute = ? WHERE user_id = ? AND profile_id = ? AND content_id = ?'
    return execute_query(query, (new_last_watched_minute, user_id, profile_id, content_id))

def delete_continue_entry(user_id, profile_id, content_id):
    query = 'DELETE FROM continue_watching WHERE user_id = ? AND profile_id = ? AND content_id = ?'
    return execute_query(query, (user_id, profile_id, content_id))
