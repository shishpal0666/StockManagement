import os

class Config:
    SECRET_KEY = os.urandom(12).hex()
    DB_NAME = 'stockdb'
    DB_USER = 'postgres'
    DB_PASSWORD = 'password'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
