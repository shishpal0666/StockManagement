from flask import Flask
from config import Config
import psycopg2

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize PostgreSQL connection
    try:
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        app.config['DB_CONNECTION'] = conn
        app.config['DB_CURSOR'] = cursor
    except Exception as e:
        print(f"Database connection error: {e}")
        exit(1)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
