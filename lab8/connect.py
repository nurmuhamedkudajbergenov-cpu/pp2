import psycopg2
from config import load_config

def get_connection():
    try:
        params = load_config()
        return psycopg2.connect(**params)
    except Exception as e:
        print(f'Ошибка: {e}')
        return None
