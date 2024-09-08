import os

class Config:
    SECRET_KEY = os.urandom(12).hex()
    DB_NAME = 'stockdb'
    DB_USER = 'User_name'
    DB_PASSWORD = 'User_password'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
