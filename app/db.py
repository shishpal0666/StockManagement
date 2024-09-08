import psycopg2
from config import Config

def get_db_connection():
    conn = psycopg2.connect(
        database=Config.DATABASE['name'],
        user=Config.DATABASE['user'],
        password=Config.DATABASE['password'],
        host=Config.DATABASE['host'],
        port=Config.DATABASE['port']
    )
    return conn
